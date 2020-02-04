from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='blog_index'),
    path('<int:blog_id>/',views.detail, name='blog_detail'),
]