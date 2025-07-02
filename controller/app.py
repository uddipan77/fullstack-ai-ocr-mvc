from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import requests

MODEL_API_URL = "https://uddipan107-ocr-dimt-model.hf.space/infer"  # Your model's API

app = FastAPI()

@app.post("/frontend_infer")
async def frontend_infer(
    image_file: UploadFile = File(...),
    json_file: UploadFile = File(...),
):
    files = {
        "image_file": (image_file.filename, await image_file.read(), "image/png"),
        "json_file": (json_file.filename, await json_file.read(), "application/json"),
    }
    try:
        response = requests.post(MODEL_API_URL, files=files)
        return JSONResponse(content=response.json(), status_code=response.status_code)
    except Exception as e:
        return JSONResponse(content={"error": f"Failed to contact model API: {e}"}, status_code=500)

@app.get("/")
def root():
    return {"msg": "Backend proxy is up!"}