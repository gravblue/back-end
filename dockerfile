FROM python:3.11-slim

WORKDIR /app

# Install sistem dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# ⚠️ Install torch versi CPU dari repo resmi PyTorch
RUN pip install --upgrade pip && \
    pip install --no-cache-dir torch==2.2.2+cpu torchvision==0.17.2+cpu \
        -f https://download.pytorch.org/whl/cpu/torch_stable.html && \
    pip install --no-cache-dir -r requirements.txt

# Copy semua file proyek
COPY . .

# Jalankan uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
