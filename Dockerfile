# 🐍 Use official slim Python base image
FROM python:3.12-slim

# 🔧 Set essential environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 📁 Set work directory
WORKDIR /app

# 🧱 Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 🧾 Copy dependency files first (for caching layers)
COPY requirements.txt .

# 🧰 Install Python dependencies
RUN pip install -r requirements.txt

# 📦 Copy the rest of your app
COPY . .

# 🌐 Expose Streamlit default port
EXPOSE 8501

# 🚀 Run the Streamlit app
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
