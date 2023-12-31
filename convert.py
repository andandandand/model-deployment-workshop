import torch
import torchvision.models as models

# Load the pretrained ResNet-34 model
model = models.resnet34(pretrained=True)

# Ensure the model is in evaluation mode
model.eval()

# Define dummy input to match the input size during ONNX export
# Here, we'll create a tensor of size [1, 3, 224, 224] as a placeholder input
x = torch.randn(1, 3, 224, 224, requires_grad=True)

# Export the model to ONNX
onnx_filename = "models/resnet34.onnx"
torch.onnx.export(model,                     # model being run
                  x,                         # model input (or a tuple for multiple inputs)
                  onnx_filename,             # where to save the model (can be a file or file-like object)
                  export_params=True,        # store the trained parameter weights inside the model file
                  opset_version=11,          # the ONNX version to export the model to
                  do_constant_folding=True)  # whether to execute constant folding for optimization
