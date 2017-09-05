FROM quay.io/keboola/docker-custom-python:1.4.2

WORKDIR /home

# Initialize the transformation runner
COPY . /home/

# Run the application
ENTRYPOINT python ./main.py --data=/data/
