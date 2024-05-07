import cv2
import threading
import time
from django.conf import settings
from queue import Queue
                     
class CameraHandler:
    _instance = None
    
    def __init__(self):
        self.video_opened = False
        self.sub_idx = 0
        self.subscribers = []
        self.open_video()
        self.start_capturing()
        
    def open_video(self):
        self.video_handler = cv2.VideoCapture(0)
        self.video_handler.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
        self.video_handler.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
        self.video_opened = True
        
    def close_video(self):
        self.video_handler.release()
        self.video_opened = False
        
    def start_capturing(self):
        self.capture_thread = threading.Thread(
        target=self.update_subscribers, args=())
        self.capture_thread.start()
        
    def fetch_frame(self):
        grabbed, frame  = self.video_handler.read()
        if grabbed:
            _, frame = cv2.imencode('.jpg', frame)
        return grabbed, frame
    
    def add_subscriber(self, subscriber):
        self.sub_idx += 1
        subscriber.idx = self.sub_idx
        self.subscribers.append(subscriber)
        
    def remove_subscriber(self, subscriber):
        self.subscribers = [s for s in self.subscribers if s.idx != subscriber.idx]
        
    def update_subscribers(self):
        while True:
            if len(self.subscribers) > 0:
                if not self.video_opened:
                    self.open_video()
                grabbed, frame = self.fetch_frame()
                if not grabbed:
                    continue
                payload = frame.tobytes()
                data = b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + payload + b'\r\n\r\n'
                for sub in self.subscribers:
                    sub.new_data(data)
            else:
                if self.video_opened:
                    self.close_video()
                time.sleep(1)
    
    @staticmethod
    def get_instance():
        if CameraHandler._instance is None:
            CameraHandler._instance = CameraHandler()
        return CameraHandler._instance
            
class CameraConsumer:
    def __init__(self, idx=0):
        self.idx = idx
        self.frame_buffer = Queue()
        self.camera_handler = None
        
    def subscribe(self, camera_handler):
        self.camera_handler = camera_handler
        self.camera_handler.add_subscriber(self)
        
    def new_data(self, data):
        self.frame_buffer.put(data)
        
    def image_generator(self):
        while True:
            try:
                yield self.frame_buffer.get()
            except: #Broken pipe
                if self.camera_handler is not None:
                    self.camera_handler.remove_subscriber(self)