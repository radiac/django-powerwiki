#!/bin/bash
cd /project/example

export PYTHONPATH=..

./manage.py migrate
./manage.py runserver 0:8000
