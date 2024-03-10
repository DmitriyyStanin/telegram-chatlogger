# Use a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the application code to the container
COPY . /app

# Install any dependencies needed for the application
RUN pip install -r requirements.txt

# Expose the port the application runs on
EXPOSE 8000

# Set the command to run the application
CMD ["python", "app.py"]

