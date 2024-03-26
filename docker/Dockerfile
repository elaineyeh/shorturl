# pull official base image
FROM public.ecr.aws/docker/library/python:3.8

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y netcat-traditional

# copy entrypoint.sh
COPY ./docker/entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# create gunicorn log, static and media folder
RUN mkdir -p log
RUN mkdir -p collect_static
RUN mkdir -p media

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]