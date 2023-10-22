# Serving FastAPI apss through Uvicorn

To run a FastAPI application using Uvicorn, we  use the `uvicorn` command-line utility followed by the name of the Python module containing your FastAPI app, as well as the variable name of the FastAPI instance. The syntax is like this:

```bash
uvicorn module_name:app_variable --port port_number
```

For us to run a FastAPI application contained in a file named `check.py` on port 9090, we can execute the following command in your terminal:

```bash
uvicorn check:app --port 9090
```

Make sure you are in the same directory as `check.py`, or provide the full path to it. This will start the Uvicorn server and your FastAPI app should be accessible at `http://127.0.0.1:9090`, which is the default value for `--host`. 

```bash
uvicorn check:app --host 127.0.0.1 --port 9090
```

To specify the host when running your FastAPI application with Uvicorn, we can use the `--host` flag, like so:
- For `127.0.0.1`: `uvicorn check:app --host 127.0.0.1 --port 9090`
- For `0.0.0.0`: `uvicorn check:app --host 0.0.0.0 --port 9090`


## The Swagger UI

Swagger UI is an interactive API documentation tool that is automatically generated by FastAPI for your application. It provides a web-based user interface where you can explore all the API endpoints defined in your FastAPI app. Swagger UI allows you to:

1. View all available API routes, including HTTP methods, query parameters, request bodies, and response models.
2. Execute API calls directly from the browser, making it easier to test and debug your endpoints.
3. View detailed descriptions and constraints if you've added documentation strings and validation to your FastAPI app's code.

By default, Swagger UI is available at the `/docs` endpoint of your FastAPI application (e.g., `http://127.0.0.1:9090/docs` if running locally on port 9090). We can interact with it via the web browser, and it's often enabled in development environments for easier testing and debugging.

In the `check.py` file, we only have a GET method. When we work getting predictions from a model, we need to implement POST. 

## Using 127.0.0.1 vs 0.0.0.0 as --host 

Both 0.0.0.0 and 127.0.0.1 are IP addresses, but they serve different purposes, especially in the context of binding a server to an address.

### 127.0.0.1
- **Loopback Address**: This is the loopback address for the local machine. It's used to establish network connections with services running on the same machine.
- **Accessibility**: When you bind a server to 127.0.0.1, the server will only be accessible from the same machine.
- **Security**: Generally safer to use for development, as it does not expose the server to the external network.
  
### 0.0.0.0
- **Wildcard Address**: This is a wildcard address that listens on all available network interfaces.
- **Accessibility**: When you bind a server to 0.0.0.0, it will be accessible from any IP address that routes to the machine, including both localhost and external IP addresses.
- **Security**: Using 0.0.0.0 can be risky in unprotected networks, as it makes the server accessible from any external network that can reach the machine.

#### In the context of FastAPI and Uvicorn:
- Binding to `127.0.0.1` will make your server accessible only at `http://127.0.0.1:port_number`, and only to clients running on the same machine.
- Binding to `0.0.0.0` will make your server accessible at `http://external_ip_address:port_number` and `http://127.0.0.1:port_number`, to any client that can reach `external_ip_address`.

