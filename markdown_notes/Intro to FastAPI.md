# What is FastAPI? 


FastAPI is a modern web framework for building APIs with Python, based on standard Python type hints and asynchronous programming. The most important concept to get started with it are routes. 

## Routes in FastAPI

In FastAPI, a "route" refers to a specific endpoint in your API, which is associated with a Python function to execute when that endpoint is accessed. Essentially, a route specifies how to respond to a particular [HTTP request method](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) (like GET, POST, PUT, etc.) for a given URL path in the application.

### Anatomy of a Route

A FastAPI route consists of the following elements:

1. **HTTP Method**: The type of HTTP request method (GET, POST, PUT, DELETE, etc.).
2. **Path**: The URL path (for example, `/items` or `/users/{user_id}`) that the route will respond to.
3. **Decorator**: A Python decorator that combines the HTTP method and path, and associates them with the subsequent Python function.
4. **Route Handler Function**: The Python function that is executed when a request matches the specified path and method. This function contains the logic for what should happen when the route is accessed and can return a response.

Here's an example to clarify:
```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

- **HTTP Method**: GET
- **Path**: `/items/{item_id}`
- **Decorator**: `@app.get("/items/{item_id}")`
- **Route Handler Function**: `async def read_item(item_id: int)`

### How it Works:

1. When a client (like a web browser) sends an HTTP GET request to the URL that matches `/items/{item_id}`, the FastAPI application will invoke `read_item`.
2. The function parameter `item_id` will automatically get the value from the URL path.
3. The Python function executes its logic (in this case, it simply returns a dictionary) and the response is sent back to the client.

Routes serve as the fundamental building blocks for your FastAPI application, allowing you to define the behavior of your API for various URL paths and HTTP methods.


### Understanding our Basic Example

 Here, let's break down the key concepts using the provided commented file.

```python
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
```


### Import FastAPI
```python
from fastapi import FastAPI
```
The first line imports the `FastAPI` class. This class is the foundation for creating a FastAPI application.

### Create an Instance of FastAPI
```python
app = FastAPI()
```
An instance of the FastAPI class is created and stored in the variable `app`. This instance enables you to define routes and set up various configurations for your application.

### Define a Route
```python
@app.get("/")
async def root():
    return {"message": "Hola Mamá", "status": "ok", "code": 200, "data": {"name": "Mamá", "age": 71}}
```
- `@app.get("/")`: This is a decorator that tells FastAPI to handle HTTP GET requests at the root URL ("/"). 
- `async def root()`: This defines an asynchronous function named `root`. Making it asynchronous allows for better performance, especially when dealing with IO-bound or high-latency operations.
  
### Return Response
Inside the function `root`, a dictionary is returned. FastAPI takes care of converting this dictionary into a JSON response. Here, the JSON will have keys like "message", "status", "code", and "data".

#### Key Takeaways:
1. FastAPI is based on Python type hints and is optimized for asynchronous programming.
2. FastAPI allows for easy route definition through decorators.
3. It automatically converts Python dictionaries to JSON responses, reducing boilerplate code.
4. FastAPI is highly extensible and can integrate with various other Python libraries and tools.

