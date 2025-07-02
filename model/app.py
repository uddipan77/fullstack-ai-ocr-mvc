import os
import json
from io import BytesIO
from PIL import Image
import torch
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from huggingface_hub import hf_hub_download
from transformers import (
    AutoProcessor,
    LayoutLMv3Model,
    T5ForConditionalGeneration,
    AutoTokenizer
)

app = FastAPI()

# ── 1) CONFIG & CHECKPOINT ────────────────────────────────────────────────
HF_REPO = "Uddipan107/layoutlmv3_base_T5_small_finetuned"
CKPT_NAME = "pytorch_model.bin"

ckpt_path = hf_hub_download(repo_id=HF_REPO, filename=CKPT_NAME)
ckpt = torch.load(ckpt_path, map_location="cpu")

# ── 2) BUILD MODELS ───────────────────────────────────────────────────────
processor = AutoProcessor.from_pretrained(
    "microsoft/layoutlmv3-base", apply_ocr=False
)
layout_model = LayoutLMv3Model.from_pretrained("microsoft/layoutlmv3-base")
layout_model.load_state_dict(ckpt["layout_model"], strict=False)
layout_model.eval().to("cpu")

t5_model = T5ForConditionalGeneration.from_pretrained("t5-small")
t5_model.load_state_dict(ckpt["t5_model"], strict=False)
t5_model.eval().to("cpu")

tokenizer = AutoTokenizer.from_pretrained("t5-small")

proj_state = ckpt["projection"]
projection = torch.nn.Sequential(
    torch.nn.Linear(768, t5_model.config.d_model),
    torch.nn.LayerNorm(t5_model.config.d_model),
    torch.nn.GELU()
)
projection.load_state_dict(proj_state)
projection.eval().to("cpu")

if t5_model.config.decoder_start_token_id is None:
    t5_model.config.decoder_start_token_id = tokenizer.bos_token_id or tokenizer.pad_token_id
if t5_model.config.bos_token_id is None:
    t5_model.config.bos_token_id = t5_model.config.decoder_start_token_id

# ── 3) INFERENCE ─────────────────────────────────────────────────────────
def infer_from_files(image_file: UploadFile, json_file: UploadFile):
    # Read image
    image_bytes = image_file.file.read()
    img_name = os.path.basename(image_file.filename)

    # Parse the NDJSON file, find entry
    entry = None
    for line in json_file.file:
        if not line.strip():
            continue
        obj = json.loads(line.decode('utf-8').strip())
        if obj.get("img_name") == img_name:
            entry = obj
            break

    if entry is None:
        return {"error": f"No JSON entry for: {img_name}"}

    words = entry["src_word_list"]
    boxes = entry["src_wordbox_list"]

    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    enc = processor([img], [words], boxes=[boxes], return_tensors="pt", padding=True, truncation=True)
    pixel_values = enc.pixel_values.to("cpu")
    input_ids = enc.input_ids.to("cpu")
    attention_mask = enc.attention_mask.to("cpu")
    bbox = enc.bbox.to("cpu")

    with torch.no_grad():
        out = layout_model(
            pixel_values=pixel_values,
            input_ids=input_ids,
            attention_mask=attention_mask,
            bbox=bbox
        )
        seq_len = input_ids.size(1)
        text_feats = out.last_hidden_state[:, :seq_len, :]
        proj_feats = projection(text_feats)
        gen_ids = t5_model.generate(
            inputs_embeds=proj_feats,
            attention_mask=attention_mask,
            max_length=512,
            decoder_start_token_id=t5_model.config.decoder_start_token_id
        )

    result = tokenizer.decode(gen_ids[0], skip_special_tokens=True)
    return {"result": result}

# ── 4) FASTAPI ENDPOINT ──────────────────────────────────────────────────
@app.post("/infer")
async def infer_api(
    image_file: UploadFile = File(..., description="The image file"),
    json_file: UploadFile = File(..., description="The NDJSON file"),
):
    output = infer_from_files(image_file, json_file)
    return JSONResponse(content=output)

@app.get("/")
def healthcheck():
    return {"message": "OCR FastAPI server is running."}
