from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
import torch
from PIL import Image
import io
import os
import tempfile

os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'

model = Qwen2VLForConditionalGeneration.from_pretrained(
    "prithivMLmods/Qwen2-VL-OCR-2B-Instruct",
    torch_dtype=torch.float16,  
    device_map="auto",
)


processor = AutoProcessor.from_pretrained("prithivMLmods/Qwen2-VL-OCR-2B-Instruct")

app = FastAPI()

@app.post("/extract-text/")
async def extract_text(file: UploadFile = File(...)):
    
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
                {"type": "text", "text": "Extract the text from the ID image"},
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

        return JSONResponse(content={"extracted_text": output_text})

    except RuntimeError as e:
        if 'out of memory' in str(e):
            return JSONResponse(content={"error": "CUDA out of memory. Try reducing the batch size or using mixed precision."}, status_code=500)
        else:
            raise e
    finally:
        
        os.remove(temp_file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)