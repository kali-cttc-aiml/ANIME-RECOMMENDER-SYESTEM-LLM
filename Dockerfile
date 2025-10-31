## -------------------------------
## Parent image
## -------------------------------
FROM python:3.12-slim

## -------------------------------
## Essential environment variables
## -------------------------------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

## -------------------------------
## Work directory inside the container
## -------------------------------
WORKDIR /app

## -------------------------------
## Install system dependencies
## -------------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

## -------------------------------
## Copy all project files
## -------------------------------
COPY . .

## -------------------------------
## Install PyTorch (CPU version)
## -------------------------------
RUN pip install --no-cache-dir torch==2.9.0+cpu torchvision==0.20.0+cpu torchaudio==2.9.0+cpu \
    -f https://download.pytorch.org/whl/torch_stable.html

## -------------------------------
## Install remaining dependencies
## -------------------------------
RUN pip install --no-cache-dir -e .

## -------------------------------
## Expose Streamlit port
## -------------------------------
EXPOSE 8501

## -------------------------------
## Run the Streamlit app
## -------------------------------
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
