#!/bin/bash

export OWN_IP="http://$(hostname -I)"
echo $OWN_IP
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
