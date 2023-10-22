A Dockerfile is a script composed of various instructions to automate the building of Docker images.

We use the following Dockerfile. We will break it down line by line. 

```yaml
# Use the slim base image
FROM python:3.8-slim AS build

# create the app user
RUN useradd -m app

# create the appropriate directories
ENV HOME="/home/app"
ENV API_SRC_DIR="${HOME}/src"
ENV API_MODEL_DIR="${HOME}/models"

WORKDIR $HOME

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libzbar-dev \
    ffmpeg \
    libsm6 \
    libxext6 \
    libmagic1 && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt $API_SRC_DIR/requirements.txt
RUN pip install --no-cache-dir -r $API_SRC_DIR/requirements.txt

# Use a separate stage for the final image
FROM python:3.8-slim

# Set the appropriate directories in the final stage
ENV HOME="/home/app"
ENV API_SRC_DIR="${HOME}/src"
ENV API_MODEL_DIR="${HOME}/models"

WORKDIR $HOME

COPY --from=build /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

# Copy system dependencies
COPY --from=build /usr/lib/x86_64-linux-gnu /usr/lib/x86_64-linux-gnu
COPY --from=build /lib/x86_64-linux-gnu /lib/x86_64-linux-gnu

# Copy the created user and set permissions
COPY --from=build /etc/passwd /etc/passwd
COPY --from=build /etc/group /etc/group
COPY --from=build /home/app /home/app

# Copy application files
COPY --chown=app:app models $API_MODEL_DIR
COPY --chown=app:app src $API_SRC_DIR

USER app

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "80"]

```

A Dockerfile is a script composed of various instructions to automate the building of Docker images. Each line serves a specific purpose in this process.

1. **`FROM python:3.8-slim AS build`**: This line specifies the base image that will be used for the build. In this case, it's a slim version of Python 3.8. The `AS build` part defines this stage of the build as "build," so you can refer back to it later.

2. **`RUN useradd -m app`**: This command adds a new user named "app" to the container and creates a home directory for this user. The `-m` flag specifies that a home directory should be created.

3. **`ENV HOME="/home/app"`**: Sets the `HOME` environment variable to "/home/app."

4. **`ENV API_SRC_DIR="${HOME}/src"`**: Sets `API_SRC_DIR` to point to the `src` directory in the `HOME` directory.

5. **`ENV API_MODEL_DIR="${HOME}/models"`**: Similar to above, but for a `models` directory.

6. **`WORKDIR $HOME`**: Sets the working directory for the subsequent instructions to `$HOME`, which is "/home/app."

7. **`RUN apt-get update && ...`**: This installs several system dependencies required for the application. It removes package lists afterwards to reduce image size.

8. **`COPY requirements.txt $API_SRC_DIR/requirements.txt`**: Copies `requirements.txt` from the host machine into `$API_SRC_DIR/requirements.txt` in the container.

9. **`RUN pip install --no-cache-dir -r $API_SRC_DIR/requirements.txt`**: Installs Python dependencies listed in `requirements.txt`.

10. **`FROM python:3.8-slim`**: Starts a new build stage. This time, without the `AS build` flag.

11. **`ENV HOME="/home/app"`, `ENV API_SRC_DIR="${HOME}/src"`, `ENV API_MODEL_DIR="${HOME}/models"`**: These set environment variables just like before, but in the new stage.

12. **`WORKDIR $HOME`**: Sets the working directory in this new stage as well.

13. **`COPY --from=build /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages` etc.**: These commands copy specific files and directories from the previous build stage into the current one. This helps in reducing the final image size by only taking what's needed.

14. **`USER app`**: Sets the default user for the container to "app."

15. **`CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "80"]`**: Specifies the command that will be run when the container starts. This command runs a Uvicorn server hosting a FastAPI application.

This Dockerfile employs multi-stage builds (`AS build` and the subsequent stage) to minimize the final image size. The first stage installs all the required dependencies and the second stage copies only what is needed to run the application.
