FROM python:3.8.1-buster

RUN apt-get update && apt-get install pwgen

# Create User to prevent running as root
RUN useradd --system --shell /bin/bash --password "$(pwgen -n 32 -s -1)" app

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY myBlog /usr/src/app/

# Chown the app directory to the user
RUN chown -R app:app /usr/src/app

USER app
RUN echo $(whoami)
CMD ["gunicorn","myBlog.wsgi","--bind", "0.0.0.0:8000"]
