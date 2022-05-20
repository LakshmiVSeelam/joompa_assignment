from django.urls import path
from .views import homePageView, postData, generateexercise

urlpatterns = [
    path("home", homePageView, name="home"),
    path("", homePageView, name="home"),
    path('postData', postData, name = 'validate'),
    path('generateexercise', generateexercise, name = 'generateexercise')
]