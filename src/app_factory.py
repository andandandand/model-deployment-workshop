from fastapi import FastAPI
import onnxruntime as rt


def create_app():
    app = FastAPI(
        title="FastAPI + ONNX Runtime Demonstration",
        description="A simple API that uses ONNX Runtime to make predictions",
        version="0.1",
    )

    @app.on_event("startup")
    async def startup_event():
        # Load ONNX model and create a runtime session
        app.state.session = rt.InferenceSession("models/resnet34.onnx")

    @app.on_event("shutdown")
    async def shutdown_event():
        # Optionally, add any necessary cleanup here
        pass

    return app
