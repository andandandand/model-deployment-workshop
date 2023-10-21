from typing import Dict
from fastapi import UploadFile
from pydantic import BaseModel, validator
from fastapi import HTTPException


class ImageUpload(BaseModel):
    file: UploadFile

    @validator('file', pre=True, always=True)  # use pre=True to validate before other validators
    def validate_file_size(cls, file: UploadFile) -> UploadFile:
        # Validate file size
        file_size = len(file.file.read())
        max_file_size = 5 * 1024 * 1024  # 5 MB
        if file_size > max_file_size:
            raise HTTPException(status_code=413,
                                detail=f"File size exceeds limit of {max_file_size / (1024 * 1024)} MB")

        # Make sure to reset the file's position after reading
        file.file.seek(0)
        return file

    @validator('file')
    def validate_file_type(cls, file: UploadFile) -> UploadFile:
        # Validate mimetype
        valid_mimetypes = ["image/jpeg", "image/png", "image/gif"]
        if file.content_type not in valid_mimetypes:
            raise HTTPException(status_code=415,
                                detail=f"Invalid file type. Allowed types: {', '.join(valid_mimetypes)}")

        return file


class PredictionResponse(BaseModel):
    probabilities: Dict[str, float]
