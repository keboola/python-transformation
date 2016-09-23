FROM quay.io/keboola/base-python:3.5.2-a
MAINTAINER Ondrej Popelka <ondrej.popelka@keboola.com>

WORKDIR /home

# Initialize the transformation runner
COPY . /home/

RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
		python-numpy \
		python-scipy \
		python-matplotlib \
		ipython \
		python-pandas \
		python-sympy \
		python-nose \
		g++ \
	&& rm -rf /var/lib/apt/lists/*

# Install some commonly used packages and the Python application
RUN pip install --no-cache-dir --ignore-installed \
		httplib2 \
		ipython \
		matplotlib \
		numpy \		
		pandas \
		pymongo \
		PyYaml \
		pytest-cov \
	&& pip install --upgrade --no-cache-dir --ignore-installed --cert=/tmp/cacert.pem git+git://github.com/keboola/python-docker-application.git@1.1.0

# Run the application
ENTRYPOINT python ./main.py --data=/data/

