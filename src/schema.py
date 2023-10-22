from typing import Dict
from fastapi import UploadFile
from pydantic import BaseModel, validator
from fastapi import HTTPException
from PIL import Image
import io


class ImageUpload(BaseModel):
    file: UploadFile

    @validator('file')
    def validate_file(cls, file: UploadFile) -> UploadFile:
        # Validate mimetype
        valid_mimetypes = ["image/jpeg", "image/png", "image/gif"]
        if file.content_type not in valid_mimetypes:
            raise HTTPException(status_code=415,
                                detail=f"Invalid mimetype {file.content_type}. ")

        # Validate file size
        file_bytes = file.file.read()
        max_file_size = 5 * 1024 * 1024  # 5 MB
        if len(file_bytes) > max_file_size:
            raise HTTPException(status_code=413,
                                detail=f"File size exceeds limit of {max_file_size / (1024 * 1024)} MB")

        # Validate image content
        try:
            with Image.open(io.BytesIO(file_bytes)) as img:
                img.verify()
        except Exception:
            raise HTTPException(status_code=415,
                                detail=f"Invalid image content")

        # Make sure to reset the file's position after reading
        file.file.seek(0)
        return file


class PredictionResponse(BaseModel):
    probabilities: Dict[str, float]
