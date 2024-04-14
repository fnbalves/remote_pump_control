import serial
from django.conf import settings

class ArduinoHandler:
    _instance = None
    
    def __init__(self):
        self.ser = serial.Serial(settings.ARDUINO_PORT, baudrate=settings.ARDUINO_BAUDRATE)
        
    def activate_pump(self):
        self.ser.write(settings.PUMP_ACTIVATION_CHAR.encode())

    @staticmethod
    def get_instance():
        if ArduinoHandler._instance is None:
            ArduinoHandler._instance = ArduinoHandler()
        return ArduinoHandler._instance