from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render

def index(request):
    return HttpResponse("Страница магазина Дом лесной ведьмы.")
