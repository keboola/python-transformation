FROM quay.io/keboola/base-python:3.5.1-c
MAINTAINER Ondrej Popelka <ondrej.popelka@keboola.com>

WORKDIR /home

# Initialize the transformation runner
COPY . /home/

# Install some commonly used packages and the Python application
RUN pip install --no-cache-dir \
		PyYaml \
		httplib2 \
		pymongo \
		ipython \
		numpy \
		scipy \
	&& pip install --upgrade git+git://github.com/keboola/python-docker-application.git

# Run the application
ENTRYPOINT python ./main.py --data=/data/
