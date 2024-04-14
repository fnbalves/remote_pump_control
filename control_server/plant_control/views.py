from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView, status
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .camera import *
from .arduino import *

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
        print('OPENED STREAM')
        camera_handler = CameraHandler.get_instance()
        while True:
            grabbed, frame = camera_handler.fetch_frame()
            if not grabbed:
                print('SKIPPED')
                continue
            payload = frame.tobytes()
            yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + payload + b'\r\n\r\n')
    
    def get(self, *args, **kwargs):
        try:
            return StreamingHttpResponse(CameraStream.image_gen(), content_type="multipart/x-mixed-replace;boundary=frame")
        except:
            return JsonResponse({"status": "error", "description": 
                "Failed to open camera"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
@method_decorator(user_passes_test(test_user_authenticated), name='dispatch')       
class ControlPage(TemplateView):
    template_name = 'control_view.html'
    
class SendWater(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, **kwargs):
        arduino_handler = ArduinoHandler.get_instance()
        arduino_handler.activate_pump()
        return JsonResponse({"status": "ok", "description": "Water sent"}, status=status.HTTP_200_OK)
            
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, **kwargs):
        logout(request)
        return redirect("/login/")