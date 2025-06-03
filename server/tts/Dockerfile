FROM python:3.11-slim
ENV COQUI_TOS_AGREED=1
RUN apt-get update
RUN apt-get install -y ffmpeg libsndfile1 libgl1 && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir \
    torch==2.2.2 --index-url https://download.pytorch.org/whl/cu118 \
    torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cu118
RUN pip install --no-cache-dir \
    transformers==4.47.0 \
    coqui-tts==0.26.2 \
    fastapi uvicorn[standard] numpy
RUN tts --model_name tts_models/multilingual/multi-dataset/xtts_v2
WORKDIR /app
COPY server/tts/tts_service.py /app
COPY server/tts/data/speakers* /data/speakers

CMD ["python", "-m", "uvicorn", "tts_service:app", "--host", "0.0.0.0", "--port", "8300"]
