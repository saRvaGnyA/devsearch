from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.


def projects(request):
    return HttpResponse('Here we will list our projects')


def project(request, pk):
    return HttpResponse(f'This is project {pk}')
