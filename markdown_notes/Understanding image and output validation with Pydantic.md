# Understanding image and output validation with Pydantic

Consider the [src/schema.py file](https://github.com/andandandand/model-deployment-workshop/blob/master/src/schema.py).

We are using this file to validate the image types and their size in bytes. 
We want the FastAPI endpoint to reject all files that are not jpeg, png, or gif. We validate this in the class `ImageUpload`, using the pydantic package.

We validate that the output is a dictionary with strings as keys and float number as values in the `PredictionReponse` class

```python
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

```

Let's go through the code line by line to understand what is being implemented and how Pydantic is being used alongside FastAPI. 

Let's go through this code piece by piece to understand what is being implemented and how the Pydantic library is being used alongside FastAPI for image validation:

1. ```from typing import Dict```
   - This line imports the `Dict` type from the `typing` module which is used for type hinting.

2. ```from fastapi import UploadFile```
   - Importing `UploadFile` class from the `fastapi` module. `UploadFile` is a class provided by FastAPI to handle file uploads.

3. ```from pydantic import BaseModel, validator```
   - From `pydantic`, the `BaseModel` and `validator` are being imported. `BaseModel` is the base class for all Pydantic models, and `validator` is a decorator for validating field values.

4. ```from fastapi import HTTPException```
   - Importing `HTTPException` class from `fastapi` which can be used to raise HTTP exceptions with custom status codes and details.

5. ```from PIL import Image```
   - Importing `Image` class from `PIL` (Python Imaging Library, now known as Pillow) to work with image files.

6. ```import io```
   - Importing the `io` module which provides facilities for dealing with various types of I/O (Input/Output).

7. 
```python
class ImageUpload(BaseModel):
    file: UploadFile
```
   - Defining a new class `ImageUpload` which inherits from `BaseModel`. It has a single field `file` of type `UploadFile`.

8. 
```python
    @validator('file')
    def validate_file(cls, file: UploadFile) -> UploadFile:
```
   * A class method `validate_file` decorated with `@validator` targeting the 'file' field. This method will be used to validate the contents of the uploaded file.

9. 
```python
        # Validate mimetype
        valid_mimetypes = ["image/jpeg", "image/png", "image/gif"]
        if file.content_type not in valid_mimetypes:
            raise HTTPException(status_code=415,
                                detail=f"Invalid mimetype {file.content_type}. ")
```
   - The first validation is on the mimetype of the file to ensure it's one of the specified image types (jpeg, png, or gif). If not, an HTTP exception with status code 415 (Unsupported Media Type) is raised.

10. 
```python
        # Validate file size
        file_bytes = file.file.read()
        max_file_size = 5 * 1024 * 1024  # 5 MB
        if len(file_bytes) > max_file_size:
            raise HTTPException(status_code=413,
                                detail=f"File size exceeds limit of {max_file_size / (1024 * 1024)} MB")
```
* Next, the file size is checked to ensure it doesn't exceed a specified maximum (5 MB in this case). If it does, an HTTP exception with status code 413 (Payload Too Large) is raised.

11. 
```python
        # Validate image content
        try:
            with Image.open(io.BytesIO(file_bytes)) as img:
                img.verify()
        except Exception:
            raise HTTPException(status_code=415,
                                detail=f"Invalid image content")
```
* The image content is validated by attempting to open the image with the PIL library and calling the `verify` method. If any exception occurs (like if the file isn't a valid image), an HTTP exception with status code 415 is raised.

12. 
```python
        # Make sure to reset the file's position after reading
        file.file.seek(0)
        return file
```
* After reading the file for validation, the file's position is reset to the beginning using `seek(0)` method, so it can be read again later. The validated `file` object is then returned.

13. 
```python
class PredictionResponse(BaseModel):
    probabilities: Dict[str, float]
```
* Lastly, a separate class `PredictionResponse` is defined, inheriting from `BaseModel`, with a single field `probabilities` which is a dictionary with string keys and float values. This class could be used to structure the response of a prediction endpoint.
