from PIL import Image
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, Depends, HTTPException
import numpy as np
import json
from src.app_factory import create_app
import onnxruntime as rt
from io import BytesIO
from fastapi import UploadFile
from fastapi import HTTPException
from src.schema import ImageUpload, PredictionResponse

app = create_app()


def preprocess_image(image: Image.Image):
    # Resize the image to 256x256 pixels
    image = image.resize((256, 256), Image.BICUBIC)

    # Center crop the image to 224x224 pixels
    width, height = image.size  # Get dimensions
    new_width, new_height = 224, 224
    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2
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


with open("models/classes.json") as f:
    label_mapping = json.load(f)
labels = [label_mapping[str(k)] for k in range(len(label_mapping))]



def get_session():
    if not hasattr(app, "state") or not hasattr(app.state, "session"):
        raise HTTPException(status_code=500, detail="ONNX Runtime session not initialized")
    return app.state.session


@app.post("/predict", response_model=PredictionResponse)
async def predict_route(image: UploadFile = Depends(ImageUpload), session: rt.InferenceSession = Depends(get_session)):
    # Read the image from the uploaded file
    image_data = image.file.file.read()
    image = Image.open(BytesIO(image_data))

    image = preprocess_image(image)

    # Get the input name for the model
    input_name = session.get_inputs()[0].name

    # Run inference
    outputs = session.run(None, {input_name: image})

    # Convert model outputs to class probabilities (assuming the output is a softmax distribution)
    probabilities = np.exp(outputs[0]) / np.sum(np.exp(outputs[0]))
    probabilities = probabilities.tolist()[0]

    # Optionally, get class labels (assuming you have a list of labels corresponding to the model's output classes)
    class_probabilities = {label: float(prob) for label, prob in zip(labels, probabilities)}

    # keep only the top 5 predictions
    class_probabilities = dict(sorted(class_probabilities.items(), key=lambda item: item[1], reverse=True)[:5])

    return JSONResponse(content=class_probabilities)
