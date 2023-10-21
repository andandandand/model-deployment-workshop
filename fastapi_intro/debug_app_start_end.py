# https://fastapi.tiangolo.com/tutorial/debugging/
from PIL import Image
import uvicorn

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import numpy as np
import onnxruntime as ort
import io
import json


def preprocess_image(image: Image.Image):
    # Resize the image to 256x256 pixels
    image = image.resize((256, 256), Image.BICUBIC)

    # Center crop the image to 224x224 pixels
    width, height = image.size   # Get dimensions
    new_width, new_height = 224, 224
    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2
    image = image.crop((left, top, right, bottom))

    # Convert the image to a NumPy array and normalize it
    image = np.asarray(image) / 255.0  # Convert to [0,1] range
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    image = (image - mean) / std

    # Transpose the dimensions to match the input shape [1, 3, 224, 224]
    image = np.transpose(image, (2, 0, 1))
    image = np.expand_dims(image, axis=0)

    # Convert the image to a float tensor
    image = image.astype(np.float32)

    return image


app = FastAPI()
ort_session = ort.InferenceSession("models/resnet34.onnx")

with open("models/classes.json") as f:
    label_mapping = json.load(f)
labels = [label_mapping[str(k)] for k in range(len(label_mapping))]


def predict(image_path, sess=ort_session):
    # Preprocess the input image
    image = preprocess_image(image_path)

    # Get the input name for the model
    input_name = sess.get_inputs()[0].name

    # Run inference
    outputs = sess.run(None, {input_name: image})

    return outputs

def softmax(x):
    e_x = np.exp(x - np.max(x))  # Subtracting np.max for numerical stability
    return e_x / e_x.sum(axis=1, keepdims=True)

@app.post("/predict")
async def predict_route(file: UploadFile):
    # Read the image from the uploaded file
    image_data = await file.read()
    image = Image.new("RGB", (512, 512))

    # Run prediction
    outputs = predict(image)

    # Convert model outputs to class probabilities (assuming the output is a softmax distribution)
    probabilities = softmax(outputs)
    
    sorted_indices = np.argsort(probabilities)[0]
    top_5_indices = sorted_indices[-5:][::-1]
    class_probabilities = {labels[index]: probabilities.squeeze()[[index]].item() for index in top_5_indices}

   
    return JSONResponse(content=class_probabilities)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)