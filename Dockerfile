FROM quay.io/keboola/docker-custom-python:2.0.4

WORKDIR /home

# Initialize the transformation runner
COPY . /home/

# Run the application
ENTRYPOINT python -u ./main.py --data=/data/
