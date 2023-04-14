from django.urls import path

from .views import TestView

urlpatterns = [
    path("", TestView.as_view()),  # It is made to see that django can see those urls
]
