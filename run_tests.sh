#!/bin/sh

export KBC_DATA_DIR=/code/test/data
cd /code/
py.test --cov=transformation --cov-report term-missing
