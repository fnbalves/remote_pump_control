#!/bin/bash

while [ ! -e /dev/video0 ]; do
	echo "Waiting for camera..."
	sleep 1
done
sudo mjpg_streamer -o "output_http.so -w ./www" -i "input_uvc.so -d /dev/video0"
