from django.urls import path
from .views import RegisterView, VerifyView, ActivationView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path('activate/<str:activation_code>/', ActivationView.as_view(), name='activate'),
]