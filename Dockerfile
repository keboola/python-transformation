FROM quay.io/keboola/docker-custom-python:4.0.2

WORKDIR /home

# Initialize the transformation runner
COPY . /home/

RUN apt-get update && apt-get install -y -qq coinor-cbc

# Run the application
ENTRYPOINT python -X faulthandler -u ./main.py --data=/data/
