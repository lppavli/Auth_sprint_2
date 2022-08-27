FROM --platform=linux/amd64 python:3.9-alpine

RUN apk update \
    && apk add build-base

COPY ./requirements.txt .

RUN pip install -U setuptools pip
RUN pip install -r requirements.txt

COPY . /app


WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/app/auth"
CMD ["gunicorn", "auth.wsgi:app", "--bind", ":8000"]
