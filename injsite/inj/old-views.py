from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	html = "Hello world. How are you?"
	return HttpResponse(html)

# Create your views here.
