from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("stream", CameraStream.as_view()),
    path("", ControlPage.as_view()),
    path("send_water/", SendWater.as_view()),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user = True,                            template_name = 'login_form.html')),
    path("logout/", LogoutView.as_view()),
]