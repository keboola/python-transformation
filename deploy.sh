#!/bin/bash

docker login -e="." -u="$QUAY_USERNAME" -p="$QUAY_PASSWORD" quay.io
docker tag keboola/python-transformation quay.io/keboola/python-transformation:$TRAVIS_TAG
docker tag keboola/python-transformation quay.io/keboola/python-transformation:latest
docker images
docker push quay.io/keboola/python-transformation:$TRAVIS_TAG
docker push quay.io/keboola/python-transformation:latest
