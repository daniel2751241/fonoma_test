# use official Python image
FROM python:3.10.2-slim

# create and set working directory
RUN mkdir -p /home/app
WORKDIR /home/app

# add new group and user and give permissions
RUN groupadd -r app && useradd -r -g app app
RUN chown -R app:app /home/app

# update pip
RUN python -m pip install pip --upgrade
RUN python -m pip install setuptools --upgrade

# create and activate environment
RUN pip install -U virtualenv
RUN python -m virtualenv env
RUN /bin/bash -c 'source /home/app/env/bin/activate'

# copy app files to container
COPY . /home/app

# install requirements
RUN pip install -r requirements/base.txt

# expose port
EXPOSE 8000

# run application
CMD ["uvicorn", "main:app"]