FROM python:3.7
# Run commands from /app directory inside container
WORKDIR /app
# Copy requirements from local to docker image
COPY requirements.txt /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# Install the dependencies in the docker image
RUN pip3 install -r requirements.txt
# Copy everything from the current dir to the image
COPY . .
