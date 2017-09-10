from django.shortcuts import render
from django.http import HttpResponse

def test(request, *args, **kwards):
    return HttpResponse('OK')

# Create your views here.