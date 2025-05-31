from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

app = FastAPI(title="alex-ai-game-reader API")

@app.get("/ping")
async def ping():
    return {"msg": "pong"}

@app.post("/read")
async def read_image(img: UploadFile = File(...)):
    data = await img.read()
    return JSONResponse({"filename": img.filename, "bytes": len(data)})
