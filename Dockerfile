# Use the official Python image from the Docker Hub
FROM python:3.12.11-alpine3.22

# RUN apt-get -y update 
# RUN apt-get -y dist-upgrade

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY . /code

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Command to run the application
CMD ["uvicorn", "--host", "0.0.0.0", "main:app"]