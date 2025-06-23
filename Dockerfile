# Use official Python base image
FROM python:3.10-slim

# Install ffmpeg and other dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all files to the container
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose the port (Render sets it via env variable)
EXPOSE 10000

# Run the Flask app
CMD ["python", "app.py"]
