FROM paddlepaddle/paddle:3.0.0-gpu-cuda11.8-cudnn8.9-trt8.6 
WORKDIR /app
COPY server/ocr/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY server/ocr/ocr_service.py /app
CMD ["uvicorn", "ocr_service:app", "--host", "0.0.0.0", "--port", "8200"]
