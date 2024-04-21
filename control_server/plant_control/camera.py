import cv2
import threading
from django.conf import settings

class CameraHandler:
    _instance = None
    
    def __init__(self):
        self.open_video()
        self.subscribers = []
        
    def open_video(self):
        self.video_handler = cv2.VideoCapture(settings.CAMERA_INDEX)
        self.video_handler.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.video_handler.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.capture_thread = threading.Thread(
        target=self.update_subscribers, args=())
        self.capture_thread.start()
        
    def fetch_frame(self):
        grabbed, frame  = self.video_handler.read()
        if grabbed:
            _, frame = cv2.imencode('.jpg', frame)
        return grabbed, frame
    
    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)
        
    def update_subscribers(self):
        while True:                        
            grabbed, frame = self.fetch_frame()
            if not grabbed:
                continue
            payload = frame.tobytes()
            data = b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + payload + b'\r\n\r\n'
            
            to_remove = []
            for sub in self.subscribers:
                try:
                    sub.send(data)
                except:
                    to_remove.add(sub)
        
            for sub in to_remove:
                self.subscribers.remove(sub)
        
    @staticmethod
    def get_instance():
        if CameraHandler._instance is None:
            CameraHandler._instance = CameraHandler()
        return CameraHandler._instance
            
