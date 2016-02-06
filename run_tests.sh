#!/bin/sh

export KBC_DATA_DIR=./test/data
py.test --cov=transformation --cov-report term-missing

read
