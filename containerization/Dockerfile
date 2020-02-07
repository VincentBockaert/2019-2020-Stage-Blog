FROM python:3.6.8-jessie
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get install -y libmysqlclient-dev
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
#VOLUME . /code/
RUN python3 -m pip install -r requirements.txt
#VOLUME . /code/
COPY . /code/
EXPOSE 8000
