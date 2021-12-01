# pull the official base image
FROM python:3.9.0-slim-buster

# set the working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install apt packages
# RUN apt-get update
# RUN apt-get install python3-dev default-libmysqlclient-dev build-essential
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .

# start app
CMD ["python", "app.py"]
