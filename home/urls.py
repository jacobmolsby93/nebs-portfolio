from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('about/', views.about, name="about"),
    path('<int:image_id>/', views.delete_image, name="delete_image"),
    path('contact/', views.contact, name="contact"),
    path('add_photo/', views.add_photo, name="add_photo"),
    path('edit/<int:image_id>/', views.edit_image, name="edit_image")
    
    
]