# collector DOCKERFILE
FROM python:3.8.0-slim-buster

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# add project contents and install dependencies
ADD . /app/
RUN pip install --requirement /app/requirements.txt

WORKDIR /app
# start app
CMD ["python", "sidious.py"]
