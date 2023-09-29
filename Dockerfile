# Use an official Python runtime as base image
FROM python:3.9

# Set the working directory in the Docker container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . /app/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:8000", "my_image_api.wsgi:application"]
