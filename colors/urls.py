from django.urls import path
from . import views


app_name = 'color'

urlpatterns = [
    path('create/color/', views.create_color, name='create_color'),
]