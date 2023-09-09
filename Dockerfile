# Use the official Django image from the DockerHub
FROM python:3.9

# Set the working directory inside docker
WORKDIR /app

# Set environment variables in the docker container
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Specify the command to run on container start
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
