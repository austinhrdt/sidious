FROM python:3.8.0-slim-buster

LABEL maintainer "Austin Hardt <austinhrdt@icloud.com>"
LABEL project "sidious"

# add project contents and install dependencies
ADD . /app/
RUN pip install --requirement /app/requirements.txt

# install ffmpeg
RUN apt update && apt install ffmpeg -y

# set workdir to /app
WORKDIR /app

# start app
CMD ["python", "sidious.py"]
