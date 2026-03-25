FROM pytorch/pytorch:2.4.0-cuda12.1-cudnn9-runtime

# System deps: ffmpeg for Whisper
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Working directory
WORKDIR /app

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip

# Force pip to own setuptools/wheel fully (overrides conda's partial install)
# so pkg_resources is reachable in build subprocesses
RUN pip install --no-cache-dir --ignore-installed setuptools wheel && \
    pip install --no-cache-dir --no-build-isolation -r requirements.txt

# App code
COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["python", "app/chatgpt_client.py"]
