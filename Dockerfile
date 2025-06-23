FROM python:3.10-slim

# Install dependencies including ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Set working directory
WORKDIR /app

# Copy app files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port for Render
EXPOSE 10000

# Run with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]
