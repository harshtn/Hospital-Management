from django.urls import path
from . import views

urlpatterns = [
    path('', views.record_list, name='record_list'),
    path('new/', views.record_create, name='record_create'),
    path('<int:pk>/', views.record_detail, name='record_detail'),
    path('<int:pk>/edit/', views.record_update, name='record_update'),
]
