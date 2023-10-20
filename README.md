# Dockerized FastAPI Template
This repository is a didactic template on serving a PyTorch model through FastAPI. 
As an example, it serves ResNet34 model for image classification. You can find the model in `models/` directory.  

## Project Structure

- `src/`: Python source code.
  - `api.py`: Main FastAPI application file.
- `models/`: Models directory.
  - `resnet34.onnx`: ResNet34 model for image classification.
- `Dockerfile`: Specifies how to build the Docker image.
- `docker-compose.yaml`: Docker Compose file to run the service.
- `Makefile`: Contains shortcuts for building and running Docker containers.
- `requirements.txt`: Lists the Python dependencies.

## Getting Started


### Prerequisites

Ensure you have the following installed on your system:

- [Anaconda](https://www.anaconda.com/download)
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Build and Run the Service

1. Clone this repository:
    ```sh
    git clone https://github.com/andandandand/model-deployment-workshop
    ```
2. Navigate to the project directory:
    ```sh
    cd model-deployment-workshop
    ```
3. Build the Docker image:
    ```sh
    make build
    ```

4. Run the Docker container:
    ```sh
    make run
    ```

5. Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to view the Swagger UI.

## Development
To facilitate development, a volume is mapped from the `src/` directory on your host to the corresponding directory in the container, allowing for changes made to the local source files to be immediately reflected inside the container.  

## License
This project is licensed under the MIT License - see the LICENSE.md file for details 

## Development Suitability and Security Considerations

### Development Suitability
This project is primarily configured and optimized as a template or starting point and may not be immediately suited for development or production environments without further modifications and configurations. Developers are encouraged to review and modify configurations, dependencies, and other settings to better suit the development or production environment requirements and to comply with best practices and organizational policies.

### Security Considerations
This template does not implement additional security measures, and the users are strongly encouraged to assess and implement suitable security controls, practices, and measures fitting their use case, especially when deploying in a production environment. This includes, but is not limited to, securing API endpoints, implementing proper authentication and authorization mechanisms, securing data in transit and at rest, and regularly updating dependencies to mitigate known vulnerabilities.

Users should also review and adjust user permissions within the Docker containers and on the host system to adhere to the principle of least privilege, ensuring that services and users only have the minimum level of access—or permissions—needed to accomplish a task.

Remember that deploying insecure applications and services could lead to various security issues, including unauthorized access, data leakage, and legal ramifications, depending on the nature and sensitivity of the data processed by the application.

## Acknowledgements
- [FastAPI](https://fastapi.tiangolo.com/)
- [Docker](https://www.docker.com/)

