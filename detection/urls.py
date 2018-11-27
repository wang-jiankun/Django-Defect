from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('detection/', views.detection_view, name='detection_log'),
    path('defect/', views.defect_view, name='defect_image'),
    path('detection/log/', views.log_search, name='log_search'),
    path('defect/class/', views.defect_search, name='defect_search'),
]
