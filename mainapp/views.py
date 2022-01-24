from django.http.response import HttpResponse
from django.shortcuts import render

def IndexView(request):
    return render(request, 'mainapp/index.html')
