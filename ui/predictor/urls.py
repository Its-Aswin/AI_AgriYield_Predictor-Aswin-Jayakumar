from django.urls import path
from . import views

urlpatterns = [
    # This maps the root URL ('/') to your 'predict_view'
    path('', views.predict_view, name='predict'),
]