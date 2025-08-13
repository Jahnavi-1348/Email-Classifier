# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency file first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Run FastAPI app (change api:app to your filename:function_name)
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
