import torch
import torchvision.transforms as transforms
from torchvision import models
from torchvision.models import ResNet34_Weights

from PIL import Image
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
from io import BytesIO
import json


with open("../models/classes.json") as f:
    label_mapping = json.load(f)


transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def preprocess_image(image: Image.Image):
    image = image.convert("RGB")
    return transform(image).unsqueeze(0)

def predict(image_tensor):
    with torch.no_grad():
        output = model(image_tensor)
    _, predicted = output.max(1)
    return predicted.item()

app = FastAPI()
model = models.resnet34(weights=ResNet34_Weights.IMAGENET1K_V1)
model.eval()

@app.post("/predict/")
async def predict_image(file: UploadFile = File(...)):
    image_data = await file.read()
    image = Image.open(BytesIO(image_data))
    
    # Preprocess and predict
    input_tensor = preprocess_image(image)
    prediction = predict(input_tensor)
    prediction = label_mapping[str(prediction)]
    
    # Now try returning what we have in the notebook (top 5 predictions and their probabilities)
    return JSONResponse(content={"prediction": prediction})
