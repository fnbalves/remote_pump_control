import RPi.GPIO as GPIO
import time
import subprocess
from django.conf import settings

def setup_pins():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(settings.GPIO_USED_PIN, GPIO.OUT)
	
def run_pulse():
	GPIO.output(settings.GPIO_USED_PIN, GPIO.HIGH)
	time.sleep(settings.GPIO_TIME_TO_WAIT)
	GPIO.output(settings.GPIO_USED_PIN, GPIO.LOW)

def setup_and_run_pulse():
	setup_pins()
	run_pulse()

def clear_pin():
	setup_pins()
	GPIO.output(settings.GPIO_USED_PIN, GPIO.LOW)
		
def run_pulse_subprocess():
	command = [
	"python",
	"manage.py",
	"shell",
	"-c",
	"from plant_control.gpio import setup_and_run_pulse; setup_and_run_pulse()"
	]
	subprocess.Popen(command)

clear_pin()
