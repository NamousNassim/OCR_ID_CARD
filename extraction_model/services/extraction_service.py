from fastapi.responses import JSONResponse
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
import torch
from fastapi import UploadFile
from PIL import Image
import io
import os
import tempfile

model = Qwen2VLForConditionalGeneration.from_pretrained(
    "prithivMLmods/Qwen2-VL-OCR-2B-Instruct",
    torch_dtype=torch.float16,  
    device_map="auto",
)

processor = AutoProcessor.from_pretrained("prithivMLmods/Qwen2-VL-OCR-2B-Instruct")

async def extract_text_from_image(file: UploadFile):
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    image = image.resize((640, 480))  
    png_image = image.convert("RGB")
    
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        png_image.save(temp_file, format='PNG')
        temp_file_path = temp_file.name

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": temp_file_path},
                {"type": "text", "text": "Extract the text from the ID image specify value and the key"},
            ],
        }
    ]

    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )

    torch.cuda.empty_cache()
    inputs = {key: val.to("cuda") for key, val in inputs.items()}

    try:
        generated_ids = model.generate(**inputs, max_new_tokens=128)
        generated_ids_trimmed = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs['input_ids'], generated_ids)
        ]
        output_text = processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )

        # Parse the extracted text to JSON
        extracted_text = output_text[0]
        parsed_data = parse_extracted_text(extracted_text)

        return JSONResponse(content={"extracted_text": parsed_data})

    except RuntimeError as e:
        if 'out of memory' in str(e):
            return JSONResponse(content={"error": "CUDA out of memory. Try reducing the batch size or using mixed precision."}, status_code=500)
        else:
            raise e
    finally:
        os.remove(temp_file_path)

def parse_extracted_text(text: str) -> dict:
    lines = text.split('\n')
    data = {
        "country": lines[0] if len(lines) > 0 else "",
        "document_type": lines[1] if len(lines) > 1 else "",
        "last_name": lines[2] if len(lines) > 2 else "",
        "first_name": lines[3] if len(lines) > 3 else "",
        "birth_date": lines[5] if len(lines) > 5 else "",
        "birth_place": lines[6] if len(lines) > 6 else "",
        "id_number": lines[8] if len(lines) > 8 else "",
        "can_number": lines[9] if len(lines) > 9 else "",
        "expiry_date": lines[11] if len(lines) > 11 else "",
        "additional_info": lines[12] if len(lines) > 12 else "",
    }
    return data