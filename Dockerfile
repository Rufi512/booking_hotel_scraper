
FROM python:3.8.5
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install dependencies
RUN pip install --upgrade pip

ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/


