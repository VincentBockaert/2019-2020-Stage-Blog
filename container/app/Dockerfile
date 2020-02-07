FROM python:3.8.1-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
RUN python3 -c "import secrets;s=secrets.token_hex(4);print(s);"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY myBlog /usr/src/app/
CMD ["gunicorn","myBlog.wsgi","--bind", "0.0.0.0:8000"]
