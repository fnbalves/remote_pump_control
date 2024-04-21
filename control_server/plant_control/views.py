import traceback as tb
from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView, status
from django.views.generic import TemplateView
from django.views.decorators import gzip
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .camera import *
from .arduino import *
#from .gpio import *

def test_user_authenticated(user):
    if not settings.AUTHENTICATION_REQUIRED:
        return True
    return user.is_authenticated

class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return test_user_authenticated(request.user)

class CameraStream(APIView):
    permission_classes = [IsAuthenticated]
    
    @staticmethod
    def image_gen():
        while True:
            #try:            
                frame_data = yield
                if frame_data is not None:
                    print('GOT')
                    yield frame_data
            #except:
            #    print('Exiting image generator')
            #    break
    
    @staticmethod
    def open_image_gen():
        camera_handler = CameraHandler.get_instance()
        gen = CameraStream.image_gen()
        camera_handler.add_subscriber(gen)
        return gen
        
    @method_decorator(gzip.gzip_page)            
    def get(self, *args, **kwargs):
        return StreamingHttpResponse(CameraStream.open_image_gen(), content_type="multipart/x-mixed-replace;boundary=frame")
            
@method_decorator(user_passes_test(test_user_authenticated), name='dispatch')       
class ControlPage(TemplateView):
    template_name = 'control_view.html'
    
class SendWater(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, **kwargs):
        if not settings.USE_GPIO:
            arduino_handler = ArduinoHandler.get_instance()
            arduino_handler.activate_pump()
            pass
        else:
            #setup_pins()
            #run_pulse()
            pass
        return JsonResponse({"status": "ok", "description": "Water sent"}, status=status.HTTP_200_OK)
            
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, **kwargs):
        logout(request)
        return redirect("/login/")
