# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy the Pipfile and Pipfile.lock into the container
COPY Pipfile Pipfile.lock ./

# Install the dependencies
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of the application code into the container
COPY . .

# Set environment variables using the ENV command
ENV VERSION=1.0
ENV FLASK_APP=src/app.py
ENV PYTHONUNBUFFERED=1

# Expose the port the app runs on
EXPOSE 3000

# Define the command to run the application
CMD ["pipenv", "run", "flask", "run", "-h", "0.0.0.0", "-p", "3000"]