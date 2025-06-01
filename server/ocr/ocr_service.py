from fastapi import FastAPI, File, UploadFile
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np, io

app = FastAPI()
ocr = PaddleOCR(use_angle_cls=True, lang="en")

@app.post("/ocr")
async def run_ocr(img: UploadFile = File(...)):
    data = await img.read()
    pil = Image.open(io.BytesIO(data)).convert("RGB")
    res = ocr.ocr(np.array(pil))  # [[ [box], (text, prob) ], … ]
    out = [{"text": t[0], "prob": float(t[1]), "bbox": box} for line in res for box, t in line]
    return {"results": out}
