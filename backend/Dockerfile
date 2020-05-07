FROM tiangolo/uvicorn-gunicorn-fastapi:python3.6
COPY ./app /app/app

COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

RUN apt-get update && \
    apt-get install -y default-jdk && \
    java -version
