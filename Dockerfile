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

# copy the dependencies from the build stage
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
