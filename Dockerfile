# Use official Python base
FROM python:3.10-slim

# Set workdir
WORKDIR /code

# Install system dependencies (optional: add git if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your FastAPI app
COPY app/ ./app/

# Expose port (Hugging Face expects 7860)
EXPOSE 7860

# Run FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]