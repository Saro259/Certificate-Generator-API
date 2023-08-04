from django.urls import path
from .views import generate_certificate
from .views import verify_certificate
from .views import fetch_certificate


urlpatterns = [
    path('generate_certificate/', generate_certificate, name='generate_certificate'),
    path('verify_certificate/', verify_certificate, name='verify_certificate'),
    path('fetch_certificate/', fetch_certificate, name='fetch_certificate')
    # other URL patterns...
]