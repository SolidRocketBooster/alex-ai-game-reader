from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import httpx

app = FastAPI(title="alex-ai-game-reader API")

@app.get("/ping")
async def ping():
    return {"msg": "pong"}

@app.post("/read")
async def read(img: UploadFile = File(...)):
    async with httpx.AsyncClient() as c:
        resp = await c.post("http://ocr:8200/ocr", files={"img": (img.filename, await img.read())})
    return resp.json()
