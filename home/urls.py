from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('about/', views.about, name="about"),
    path('image/<int:image_id>/', views.delete_image, name="delete_image"),
    path('video/<int:video_id>/', views.delete_video, name="delete_video"),
    path('edit_image/<int:image_id>/', views.edit_image, name="edit_image"),
    path('edit_video/<int:video_id>/', views.edit_video, name="edit_video"),
    path('add_photo/', views.add_photo, name="add_photo"),
    path('add_video/', views.add_video, name="add_video"),
    path('contact/', views.contact, name="contact"),
    path('manage/', views.site_management, name="site_management"),    
]