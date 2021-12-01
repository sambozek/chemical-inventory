from django.http.request import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_page(request):
    return HttpResponse('<html><title>Chemical Inventory</title></html>')