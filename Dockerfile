# Official Python Alpine image from the Docker Hub
FROM python:3.9.1-alpine3.12

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Make a new directory to put our code in
RUN mkdir /opt/django_template_app

#Change the working directory
# Every command after this be run from the /template directory
WORKDIR /opt/django_template_app

# Install postgres client
RUN apk add --update --no-cache postgresql-client 

# Install individual dependencies
# so that we could avoid installing extra packages to the container

RUN apk add --update --no-cache --virtual .tmp-build-deps \
	gcc libc-dev linux-headers postgresql-dev shadow

# Copy de requirements.txt and entrypoint.sh file
COPY requirements.txt /opt/django_template_app/

COPY entrypoint.sh /opt/django_template_app/

# Upgrade pip
RUN pip install --upgrade pip

# Install the requirements.
RUN pip install -r requirements.txt

# Create an user-template user 
RUN useradd --user-group --create-home --no-log-init --shell /bin/sh user_template_app
RUN chown -R user_template_app:user_template_app /opt/django_template_app

# Remove dependencies
RUN apk del .tmp-build-deps

USER user_template_app:user_template_app

ENTRYPOINT [ "/opt/django_template_app/entrypoint.sh" ]

