FROM quay.io/keboola/docker-custom-python:1.6.1

WORKDIR /home

# Initialize the transformation runner
COPY . /home/

# Run the application
ENTRYPOINT python -u ./main.py --data=/data/
