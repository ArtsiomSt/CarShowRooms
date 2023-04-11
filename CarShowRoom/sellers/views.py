from django.shortcuts import render, HttpResponse


# Create your views here.
def test_view(request):
    return HttpResponse("test")
