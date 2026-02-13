FROM python:3.13-slim

LABEL maintainer="Ecocompteur Simulator"
LABEL description="Docker image for Ecocompteur API Simulator"

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port 80
EXPOSE 80

# Run the application
CMD ["python", "app.py"]
