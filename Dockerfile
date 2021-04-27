
FROM python:3.8.5

ENV PYTHONUNBUFFERED=1

RUN mkdir /code

COPY requirements.txt /code/
COPY . /code/

WORKDIR /code
RUN pip install -r requirements.txt

#ENTRYPOINT [ "sh","script.sh" ]