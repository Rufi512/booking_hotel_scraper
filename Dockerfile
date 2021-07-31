
FROM python:3.8.5
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/


#COPY requirements.txt /code/
#COPY . /code/
#WORKDIR /code
#RUN pip install -r requirements.txt
#ENTRYPOINT [ "sh","script.sh" ]