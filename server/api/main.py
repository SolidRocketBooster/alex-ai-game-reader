from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from starlette.responses import StreamingResponse
import httpx, re, io


app = FastAPI(title="alex-ai-game-reader API")
HTTP_TIMEOUT = httpx.Timeout(connect=10.0, read=120.0, write=30.0, pool=5.0)
OCR_MIN_LEN = 4
OCR_MIN_PROB = 0.80

@app.get("/ping")
async def ping():
    return {"msg": "pong"}

@app.post("/read")
async def read(img: UploadFile = File(...)):
    async with httpx.AsyncClient() as c:
        resp = await c.post("http://ocr:8200/ocr", files={"img": (img.filename, await img.read())})
    return resp.json()

@app.post("/speak")
async def speak(img: UploadFile = File(...), lang: str = Form("pl")):
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as c:
        ocr_resp = await c.post("http://ocr:8200/ocr", files={"img": (img.filename, await img.read())}, \
                                timeout=HTTP_TIMEOUT)
    ocr_data = ocr_resp.json().get("results", [])

    lines = [r["text"] for r in ocr_data
             if len(r["text"]) >= OCR_MIN_LEN and r["prob"] >= OCR_MIN_PROB]
    text = "  ".join(lines) or "(brak tekstu)"

    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as c:
        tts_resp = await c.post("http://tts:8300/tts", json={"text": text, "lang": lang}, \
                                timeout=HTTP_TIMEOUT)
    return StreamingResponse(io.BytesIO(tts_resp.content), media_type="audio/wav")
