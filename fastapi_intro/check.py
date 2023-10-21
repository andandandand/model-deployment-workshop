# This line imports the FastAPI class from the fastapi module. 
# FastAPI is the main class that provides all the functionalities to build and run your FastAPI application.
from fastapi import FastAPI
# Here, an instance of the FastAPI class is created and assigned to the variable app. 
# This instance represents your FastAPI application and will be used to define routes and other configurations for the application.
app = FastAPI()

# This line is a decorator that tells FastAPI to use the function defined on the next line as the handler for HTTP GET requests to the root URL ("/").
# The @app.get decorator is a shorthand for creating an instance of the fastapi.routing.Route class, and adding that instance to the FastAPI application.
@app.get("/")
# This line defines an asynchronous function named root.
# In FastAPI, route handlers are  defined as asynchronous functions to allow for asynchronous IO operations, improves performance.
async def root():
# Inside the root function, a dictionary is returned with a single key-value pair. 
# FastAPI will automatically convert this dictionary to a JSON response. The resulting JSON response will look like this: {"message": "Hola Mamá"}.
    return {"message": "Hola Mamá", 
            "status": "ok", 
            "code": 200, 
            "data": {"name": "Mamá", "age": 71}}
