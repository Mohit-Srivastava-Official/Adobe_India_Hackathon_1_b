# syntax=docker/dockerfile:1
FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY input/ ./input/
COPY output/ ./output/
COPY persona.json ./

CMD ["python", "src/main.py"]
