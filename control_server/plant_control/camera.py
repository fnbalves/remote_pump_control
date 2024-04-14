import cv2
import threading
from django.conf import settings

class CameraHandler:
    _instance = None
    
    def __init__(self):
        self.video_handler = cv2.VideoCapture(settings.CAMERA_INDEX)
        
    def fetch_frame(self):
        grabbed, frame  = self.video_handler.read()
        if grabbed:
            _, frame = cv2.imencode('.jpg', frame)
        return grabbed, frame
        
    @staticmethod
    def get_instance():
        if CameraHandler._instance is None:
            CameraHandler._instance = CameraHandler()
        return CameraHandler._instance
            