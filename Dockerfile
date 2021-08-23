FROM quay.io/keboola/docker-custom-python:4.0.2

WORKDIR /home

# Initialize the transformation runner
COPY . /home/

# Run the application
ENTRYPOINT python -X faulthandler -u ./main.py --data=/data/
