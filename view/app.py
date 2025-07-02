import gradio as gr
import requests

BACKEND_API_URL = "https://uddipan107-ocr-dimt-controller.hf.space/frontend_infer"

def ui_submit(image, json_file):
    if image is None or json_file is None:
        return "Please upload both an image and a NDJSON file."

    # image is a file path (string), so open it in binary mode
    with open(image, "rb") as img_f, open(json_file.name, "rb") as json_f:
        files = {
            "image_file": (image.split("/")[-1], img_f, "image/png"),
            "json_file": (json_file.name, json_f, "application/json"),
        }
        try:
            response = requests.post(BACKEND_API_URL, files=files)
            if response.status_code == 200:
                data = response.json()
                return data.get("result") or data.get("error") or str(data)
            else:
                return f"Backend error {response.status_code}: {response.text}"
        except Exception as e:
            return f"Error calling backend: {e}"

gr.Interface(
    fn=ui_submit,
    inputs=[
        gr.Image(type="filepath", label="Upload Image"),   # <-- corrected
        gr.File(label="Upload JSON (NDJSON)"),
    ],
    outputs="text",
    title="OCR Full-Stack Demo",
    description="Upload an image and NDJSON. The backend forwards your files to the model API and returns the result."
).launch()