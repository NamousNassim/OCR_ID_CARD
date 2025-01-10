import requests
from base64 import b64encode
from flet import Page, FilePicker, FilePickerResultEvent, Column, Text, Image, ProgressBar, ElevatedButton

# Create components
file_picker = FilePicker()
progress_bar = ProgressBar(visible=False)
image_preview = Image(width=300, height=200, fit="contain", src_base64="")  # Set initial empty value
output_text = Text(value="Upload an image to extract information.")

def handle_upload(e: FilePickerResultEvent):
    if file_picker.result is not None:
        # Get the file path
        file = file_picker.result.files[0]
        file_path = file.path

        try:
            # Read the file as bytes
            with open(file_path, "rb") as f:
                file_bytes = f.read()

            # Convert the file to base64 for the image preview
            encoded_image = b64encode(file_bytes).decode("utf-8")
            print(f"Encoded Image Base64 Length: {len(encoded_image)}")  # Debugging line

            # Prepare the Base64 string without data:image/png;base64, if it exists
            image_data = f"data:image/png;base64,{encoded_image}"
            image_preview.src_base64 = image_data

            # Update the image preview by setting src_base64 and updating it explicitly
            image_preview.update()

            # Show progress bar
            progress_bar.visible = True
            progress_bar.update()

            # Send file to FastAPI backend
            response = requests.post(
                "http://localhost:8000/extract-text/",
                files={"file": ("uploaded_image.png", file_bytes, "image/png")}, 
            )

            # Handle the response
            if response.status_code == 200:
                raw_text = response.json().get("extracted_text", [])
                
                # Process the raw text into readable lines
                formatted_text = process_text(raw_text)
                output_text.value = formatted_text
            else:
                output_text.value = f"Error: {response.status_code}, {response.text}"
        except Exception as err:
            output_text.value = f"Error: {str(err)}"
        finally:
            # Hide progress bar and update UI
            progress_bar.visible = False
            progress_bar.update()
            output_text.update()

def process_text(raw_text):
    """
    Processes the raw text from the server into a cleaner format.
    """
    # Ensure raw_text is a list, convert if necessary
    if isinstance(raw_text, str):
        lines = raw_text.replace("<|im_end|>", "").split("\n")
    elif isinstance(raw_text, list):
        lines = raw_text
    else:
        lines = []

    # Clean each line
    cleaned_lines = [line.strip() for line in lines if line.strip()]

    # Add labels for better formatting
    labels = [
        "Country:", "Document Type:", "First Name:", "Last Name:", "Date of Birth:",
        "Gender:", "Nationality:", "ID Number:", "Other Info:"
    ]

    formatted_output = []
    for i, line in enumerate(cleaned_lines):
        label = labels[i] if i < len(labels) else f"Unknown Field {i+1}:"
        formatted_output.append(f"{label} {line}")

    # Join the lines into a formatted string
    return "\n".join(formatted_output)

def main(page: Page):
    # Set page title
    page.title = "ID Card Information Extractor"
    
    # Add components to the page
    page.add(
        Column([
            Text("Upload an ID card image to extract its information:"),
            ElevatedButton("Pick a file", on_click=lambda e: file_picker.pick_files()),
            file_picker,
            progress_bar,
            image_preview,
            output_text
        ])
    )

    # Bind event
    file_picker.on_result = handle_upload

# Run the app
if __name__ == "__main__":
    import flet
    flet.app(target=main)
