from textwrap import indent
from django.urls import path
from . import views

urlpatterns = [
    path('playground/hello/', views.say_hello),
    path('playground/orm/', views.orm_test),
    path('', views.index)
]