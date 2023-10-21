## Converting a PyTorch Model to ONNX

Converting a PyTorch model to the [Open Neural Network Exchange (ONNX)](https://onnx.ai/) format offers several advantages when it comes to serving machine learning models in production:

1. **Cross-Platform Compatibility**: ONNX models can be deployed across a wide range of platforms and programming languages. This is particularly beneficial if your production stack does not natively support PyTorch.

2. **Optimization**: ONNX models are optimized for inference. Tools like ONNX Runtime provide optimized kernels that can speed up the inference time. These optimizations are sometimes hardware-specific, taking advantage of accelerators like GPUs or TPUs.

3. **Framework Agnostic**: Once a model is converted to ONNX, it can be run using any framework that supports ONNX. This allows you to transition between frameworks without retraining the model.

4. **Model Inspection**: ONNX models can be more easily visualized and inspected. This can be helpful for debugging, optimization, or for understanding the model architecture.

5. **Simplified Deployment**: ONNX Runtime simplifies the deployment pipeline. It abstracts many of the complexities involved in deploying a machine learning model, reducing the chances of errors or inconsistencies.

6. **Scalability**: ONNX models are easier to scale horizontally (i.e., across multiple machines) due to their reduced complexity and optimized nature, which may not always be straightforward with native PyTorch models.

7. **Reduced Dependencies**: An ONNX model has fewer dependencies compared to a native PyTorch model. This makes it easier to manage in a production environment where minimizing dependencies can simplify deployment and maintenance.

8. **Community Support**: The ONNX community is quite active, providing frequent updates, a broad set of tools, and extensive documentation. This can be an advantage when you need help or when you're looking to extend functionalities.

9. **Quantization Support**: ONNX has good support for quantization, which can reduce the size of the model and speed up inference without a significant loss in accuracy.

Here's a simple example to convert a PyTorch model to ONNX:

```bash
!pip install onnx -q
!pip install onnxruntime -q
```
## Turning model into ONNX format 
```python
import torch.onnx
import torchvision.models as models

# Initialize model
model = models.resnet18(pretrained=True)

# Set model to evaluation mode
model.eval()

# Define dummy input
x = torch.randn(1, 3, 224, 224)

# Export to ONNX
torch.onnx.export(model, x, "resnet18.onnx")
```

### Running Inference
```python
import onnxruntime as ort
import numpy as np
import torch

# Initialize ONNX Runtime session
ort_session = ort.InferenceSession("resnet18.onnx")

# Prepare input data (same shape as the dummy input used for exporting the model)
input_name = ort_session.get_inputs()[0].name
input_shape = (1, 3, 224, 224)
input_data = np.random.randn(*input_shape).astype(np.float32)

# Run inference
ort_inputs = {input_name: input_data}
ort_outs = ort_session.run(None, ort_inputs)

# Extract output
output_data = ort_outs[0]

# Convert ONNX Runtime output to PyTorch tensor if needed
output_tensor = torch.from_numpy(output_data)
output_tensor

```

You can find this running in the [following Colab notebook](https://colab.research.google.com/drive/1cv7M7Utut6-ym98wUKMIMignIIHENHsg#scrollTo=dPgEFGnAEF7k).

The [example tutorial notebook in the repository](https://github.com/andandandand/model-deployment-workshop/blob/master/notebooks/Running_a_Pretrained_Resnet_on_Unsplash_Images.ipynb) shows this in more detail.  
