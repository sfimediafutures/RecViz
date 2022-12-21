FROM python:3.9
ENV PYTHONBUFFERED 1
COPY ./requirements.txt /requirements.txt

RUN apt-get install libpq-dev 
RUN pip install -r /requirements.txt

RUN mkdir -pv /var/{log,run}/gunicorn/

RUN mkdir /web
COPY ./web /web
WORKDIR /web

