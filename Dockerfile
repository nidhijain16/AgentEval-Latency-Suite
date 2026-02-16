# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port if we were running a FastAPI server (common in production)
EXPOSE 8000

# Command to run the benchmark script by default
CMD ["python", "benchmarks/latency_test.py"]
