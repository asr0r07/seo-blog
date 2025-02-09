from django.urls import path
from . import views


app_name = 'products'

urlpatterns = [
    path('list/', views.product_list, name='list'),
    path('create/product', views.create_product, name='product_create'),
    path('success/review/<int:pk>/', views.success_review, name='success_review'),
    path('blog/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.product_detail, name='detail'),
]