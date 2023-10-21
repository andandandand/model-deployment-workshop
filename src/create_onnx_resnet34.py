import torch.onnx
import torchvision.models as models
from torchvision.models import ResNet34_Weights


# Initialize model
model = models.resnet34(weights=ResNet34_Weights.IMAGENET1K_V1)

# Set model to evaluation mode
model.eval()

# Define dummy input
x = torch.randn(1, 3, 224, 224)

# Export to ONNX
torch.onnx.export(model, x, "../models/resnet34.onnx")