# Use a lightweight Python image
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Install yt-dlp
RUN pip install yt-dlp

# Copy your API code
COPY app.py /app.py

# Expose the API port
EXPOSE 8080

# Run the API
CMD ["python3", "./app.py"]