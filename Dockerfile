

# Use an official Python runtime as the base image
FROM python:3.11.0-slim-buster


# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files to the working directory
COPY pyproject.toml poetry.lock /app/

COPY ./server /app/server

COPY ./main.py /app/main.py

COPY requirements.txt /app/

COPY ./alembic /app/

COPY ./alembic.ini /app/

RUN apt-get update && apt-get install -y libpq-dev


# Install the dependencies using poetry
# RUN poetry install --no-interaction --no-root
RUN pip install -r requirements.txt

# Copy the entire project to the working directory
COPY . .


# Expose the port that the FastAPI application will run on
EXPOSE 8000

# Run the FastAPI application using uvicorn
# Run the migrations and start the application
CMD python main.py
