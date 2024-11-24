# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Install build dependencies
RUN apt-get update && apt-get install -y build-essential

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install poetry && poetry --version

# Install the dependencies
RUN poetry install --no-dev --verbose --only main

# Copy the rest of the application code into the container
COPY . .

# Install Uvicorn
RUN poetry run pip install uvicorn

# Expose the port that the app runs on
EXPOSE 8000

# Command to run the application
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]