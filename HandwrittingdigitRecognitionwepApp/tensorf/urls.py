from .import views
from django.urls import path

urlpatterns = [
	
    path('', views.index, name='digit'),
    path('predit_digit/', views.predit_digit, name='predit_digit'),
    ]