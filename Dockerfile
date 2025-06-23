# Use Python base image
FROM python:3.10-slim

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Set workdir
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port
EXPOSE 10000

# Run the app
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]
