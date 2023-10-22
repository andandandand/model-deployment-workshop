# Deploying a Resnet34 Convolutional Network through FastAPI

This repository is a didactic template on serving a pretrained Resnet34 from PyTorch through FastAPI. 
We work towards turning the model tested on the [notebook here](https://github.com/andandandand/model-deployment-workshop/blob/master/notebooks/Running_a_Pretrained_Resnet_on_Unsplash_Images.ipynb) into an endpoint for deploying an image classifier.   

The Resnet34 model is created with the `convert.py` script, `make convert` will run it and place `resnet34.onnx` in the `models` folder.

We use PyTorch, GNU Make, ONNX, Docker, and Docker Compose in our sample deployment workflow. 

## Project Structure for Deployment 

- `src/`: Python source code.
  - `api.py`: Main FastAPI application file.
- `models/`: Models directory.
  - `resnet34.onnx`: ResNet34 model for image classification.
- `Dockerfile`: Specifies how to build the Docker image.
- `docker-compose.yaml`: Docker Compose file to run the service.
- `Makefile`: Contains shortcuts for building and running Docker containers.
- `requirements.txt`: Lists the Python dependencies.

The folders `fastapi_intro`, `markdown_notes`, `unsplash_images`, and `notebooks` are content for the live workshop. 
 
## Getting Started
Reading through the following notes will give you an intuition about why are we doing things like we do:
* [Resnet notebook to perform image classification (Google Colab)](https://colab.research.google.com/drive/1IoAGXNhAFW1ojLKaLz7tMRB6fLTwcVup#scrollTo=3YkOrHc-_XC3)
* [Intro to FastAPI](https://github.com/andandandand/model-deployment-workshop/blob/master/markdown_notes/Intro%20to%20FastAPI.md)
* [Serving FastAPI apps through Uvicorn](https://github.com/andandandand/model-deployment-workshop/blob/master/markdown_notes/Serving%20FastAPI%20apps%20through%20Uvicorn.md)
* [Converting PyTorch models to ONNX format for serving](https://github.com/andandandand/model-deployment-workshop/blob/master/markdown_notes/Converting%20PyTorch%20Models%20into%20ONNX%20Format%20for%20Serving.md)
* [Understanding the docker-compose.yml file](https://github.com/andandandand/model-deployment-workshop/blob/master/Understanding%20the%20docker-compose%20file.md)
* [Understanding the relationship between GNU Make and Docker Compose](https://github.com/andandandand/model-deployment-workshop/blob/master/markdown_notes/Understanding%20the%20relationship%20between%20GNU%20Make%20and%20Docker%20Compose.md)

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

3. Create the `resnet34.onnx` network on the `models` folder:
   ```sh
   make convert 
   ```
   
4. Build the Docker image:
    ```sh
    make build
    ```

5. Run the Docker container:
    ```sh
    make run
    ```

6. Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to view the Swagger UI.

## Development
To ease development, a volume is mapped from the `src/` directory on your host to the corresponding directory in the container, allowing for changes made to the local source files to be immediately reflected inside the container.  

## License
#### Authors: Antonio Rueda-Toicen, Imran Kocabiyik
#### [Berlin Computer Vision Group](https://www.meetup.com/berlin-computer-vision-group/)

[![Creative Commons License](https://i.creativecommons.org/l/by/4.0/88x31.png)](http://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

This is a tutorial repo. Please don't use it for production applications. We take no liability of any damages or losses. 

### Security Considerations
The application in this repo does not implement additional security measures, and the users are strongly encouraged to assess and implement suitable security controls, practices, and measures fitting their use case, especially when deploying in a production environment. This includes, but is not limited to, securing API endpoints, implementing proper authentication and authorization mechanisms, securing data in transit and at rest, and regularly updating dependencies to mitigate known vulnerabilities.

Users should also review and adjust user permissions within the Docker containers and on the host system to adhere to the principle of least privilege, ensuring that services and users only have the minimum level of access—or permissions—needed to accomplish a task.


## Resources
- [FastAPI](https://fastapi.tiangolo.com/)
- [Docker](https://www.docker.com/)

