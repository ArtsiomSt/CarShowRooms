from django.urls import path
from sellers.api.v1.views import test_view


urlpatterns = [
    path("", test_view),
]
