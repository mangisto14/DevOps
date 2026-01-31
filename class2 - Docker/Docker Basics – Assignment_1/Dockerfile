    # Uses a base image
    FROM python:3.9-slim
    # Set the working directory
    WORKDIR /app
    # Copy the app.py file into the container
    COPY app.py .
    # port to expose
    EXPOSE 8080
    # Command to run the application when the container starts
    CMD ["python", "app.py"]