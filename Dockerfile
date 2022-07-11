FROM python:latest
ENV DEBIAN_FRONTEND=noninteractive

RUN pip3 install redis \
    Pillow \
    Flask
