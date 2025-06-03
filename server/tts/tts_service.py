from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import Response
from TTS.api import TTS
import soundfile as sf
import numpy as np
import io, os, glob, re, torch, unicodedata
import warnings

warnings.filterwarnings(
    "ignore",
    message=r"The text length exceeds the character limit",
    module="TTS"
)

app = FastAPI()

# ── model + referencyjny głos ─────────────────────────────
MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
tts = TTS(MODEL_NAME);  tts.to(torch.device("cuda"))
REF_WAV = "/data/speakers/sample_piotr_fronczewski.wav"

# ── token-aware splitter (limit 390 tokenów) ──────────────
tok = tts.synthesizer.tts_model.tokenizer
MAX_TOK = 390
_sent_re = re.compile(r"([.!?…]+[\s\n]+)")

def clean(txt: str) -> str:
    txt = unicodedata.normalize("NFKD", txt)
    txt = txt.replace("–", "-")          # typowy myślnik
    txt = re.sub(r'[^0-9A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ .,!?\n-]', ' ', txt)
    # składamy wielokrotne spacje
    return re.sub(r'\s{2,}', ' ', txt).strip()

def split_text(txt: str, lang: str) -> list[str]:
    parts, buf = [], ""
    # 1) elementarny split po zdaniach
    for frag in _sent_re.split(txt):
        if not frag.strip():
            continue
        # 2) jeśli dodanie fragmentu przekracza limit tokenów → zamykamy bufor
        if len(tok.encode(buf + frag, lang=lang)) >= MAX_TOK:
            if buf.strip():
                parts.append(buf.strip())
            buf = frag
        else:
            buf += frag
    if buf.strip():
        parts.append(buf.strip())
    return parts

# ── FastAPI schema ────────────────────────────────────────
class Req(BaseModel):
    text: str
    lang: str = "pl"

@app.post("/tts")
def synth(r: Req):
    text = clean(r.text)
    chunks = split_text(text, r.lang)
    wavs = []
    for chunk in chunks:
        print(f'Proccessing chunk: {chunk}')
        wavs.append(tts.tts(chunk, speaker_wav=REF_WAV, language=r.lang))
    audio  = np.concatenate(wavs)
    buf = io.BytesIO()
    sf.write(buf, audio, samplerate=tts.synthesizer.output_sample_rate,
         format="WAV")
    buf.seek(0)
    return Response(buf.getvalue(), media_type="audio/wav")
