# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .
ENV PORT 8000

# Expose the port the app runs on
EXPOSE ${http_proxy}PORT

# Command to run the FastAPI app with uvicorn
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT

