#!/bin/bash

# Wait for raspberry pi to be online to get ip
until $(curl --output /dev/null --silent --head --fail http://www.google.com); do
    printf '.'
    sleep 5
done

echo "Raspberry is online"

export SERVER_URL="http://raspberrypi"
export OWN_IP="http://$(hostname -I | awk '{print $1}')"
echo $OWN_IP
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
