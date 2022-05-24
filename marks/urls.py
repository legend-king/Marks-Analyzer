from django.urls import path
from marks import views

urlpatterns = [
    path('',views.index,name='start'),
]
