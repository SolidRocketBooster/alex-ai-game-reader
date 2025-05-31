# alex-ai-game-reader

**AI‑powered screen‑reader for PC games**.  
Press a hot‑key, draw a rectangle over on‑screen text, and hear it spoken in Polish or English.

## Features
* Zero‑cheat: uses Desktop Duplication API (`dxcam`) – no DLL injection.
* PaddleOCR 3.0 for robust multi‑lingual OCR (handles fancy fonts & handwriting).
* Dual‑engine TTS:
  * **Coqui XTTS v2** – fast, low‑latency (<250 ms).
  * **Bark / Tortoise** – cinematic expressiveness for cut‑scenes.
* Language auto‑detect, voice‑cloning from a 6‑second sample, Redis audio cache.
* LAN or remote play (Opus over WebSocket, optional WireGuard tunnel).

## Quick start (dev)
```bash
git clone https://github.com/SolidRocketBooster/alex-ai-game-reader.git
cd alex-ai-game-reader
docker compose up --build
```

Full docs in `/docs/`.

## License
MIT for this repo’s code.  
See `/models/LICENSES.md` for third‑party model terms (XTTS: MPL‑2.0, Bark: MIT).
