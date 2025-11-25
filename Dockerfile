    # Use a base Python image
    FROM python:3.9-slim-buster

    # Set the working directory inside the container
    WORKDIR /code

    # Copy the requirements file and install dependencies
    COPY ./requirements.txt /code/requirements.txt
    RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

    # Copy your application code
    COPY ./app /code/app

    # Expose the port your FastAPI app listens on (default is 8000 for Uvicorn)
    EXPOSE 8000

    # Command to run your FastAPI application with Uvicorn
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]