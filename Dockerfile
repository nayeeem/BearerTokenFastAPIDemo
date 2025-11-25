FROM python:3.13

WORKDIR /code

# Install minimal OS dependencies (add libs you actually need)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /code/requirements.txt

# Upgrade pip tooling first, then install dependencies
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# Create a non-root user and give ownership
RUN useradd --create-home --home-dir /home/appuser --shell /usr/sbin/nologin appuser \
    && chown -R appuser:appuser /code
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
