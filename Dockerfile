FROM python:3.9.7-buster

ENV TZ=Asia/Tokyo

WORKDIR /work

COPY ./requiremnts.txt /work/

RUN python -m pip install --upgrade pip \
    pip install -r requiremnts.txt
