# Use an official PyTorch runtime as a parent image
FROM pytorch/pytorch:1.9.0-cuda10.2-cudnn7-runtime

# Set the working directory in the container to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir torchvision onnx

# Copy convert.py into the app
COPY convert.py .

# Run the script when the container launches
CMD ["python", "convert.py"]
