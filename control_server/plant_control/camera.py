import cv2
import threading
import time
from django.conf import settings

                     
class CameraHandler:
    _instance = None
    
    def __init__(self):
        self.video_opened = False
        self.subscribers = []
        self.open_video()
        self.start_capturing()
        
    def open_video(self):
        self.video_handler = cv2.VideoCapture(0)
        self.video_handler.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.video_handler.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
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
        print('NEW SUB', self.subscribers)
        self.subscribers.append(subscriber)
        print('NUM SUBS', len(self.subscribers))
        
    def remove_subscriber(self, subscriber):
        self.subscribers.remove(subscriber)
        
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
                #print('NUM SUBS', len(self.subscribers))
                for sub in self.subscribers:
                    sub.new_data(data)
            else:
                if self.video_opened:
                    self.close_video()
                time.sleep(1)
    
    @staticmethod
    def get_instance():
        if CameraHandler._instance is None:
            print('CREATING INSTANCE')
            CameraHandler._instance = CameraHandler()
        return CameraHandler._instance
            
class CameraConsumer:
    def __init__(self):
        self.frame_buffer = []
        self.camera_handler = None
        
    def subscribe(self, camera_handler):
        self.camera_handler = camera_handler
        self.camera_handler.add_subscriber(self)
        
    def new_data(self, data):
        self.frame_buffer.append(data)
        
    def image_generator(self):
        while True:
            try:
                if len(self.frame_buffer) > 0:
                        yield self.frame_buffer.pop()
                #else:
                #    time.sleep(1)
            except: #Broken pipe
                if self.camera_handler is not None:
                    self.camera_handler.remove_subscriber(self)