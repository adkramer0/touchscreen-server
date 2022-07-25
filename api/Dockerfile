FROM python:3.10

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN apt-get update && apt-get install subversion

RUN pip3 install --no-cache-dir --upgrade -r /src/requirements.txt

COPY ./app /src/app

CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--preload"]

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "9"]

