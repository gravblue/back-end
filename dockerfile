FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install torch versi CPU langsung dari PyTorch repo
RUN pip install --upgrade pip && \
    pip install --no-cache-dir torch==2.2.2+cpu torchvision==0.17.2+cpu \
        -f https://download.pytorch.org/whl/cpu/torch_stable.html && \
    pip install --no-cache-dir -r requirements.txt


# Copy application code
COPY . .

# Start FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
