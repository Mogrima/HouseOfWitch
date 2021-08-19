from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .models import *

menu = [{'title': "Каталог", 'url_name': 'home'},
        {'title': "О нас", 'url_name': 'about'},
        {'title': "Статьи", 'url_name': 'article'},
        
]

class ShopHome(ListView):
    model = Goods
    template_name = 'shop/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_selected'] = 0
        context['menu'] = menu
        # context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return Goods.objects.filter(is_published=True)


def about(request):
    return render(request, 'shop/about.html', {'menu': menu, 'title': 'О нас'})


def categories(request, catid):
    return HttpResponse(f"<h1>Товары по категориям</h1><p>{catid}</p>")


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена.</h1>")


class ShowArticle(ListView):
    model = Article
    template_name = 'shop/article.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Статьи'
        return context

 
def login(request):
    return HttpResponse("Авторизация")

class ShowGoods(DetailView):
    model = Goods
    template_name = 'shop/goods.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context


class GoodsCategory(ListView):
    model = Goods
    template_name = 'shop/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['menu'] = menu
        context['cat_selected'] = context['posts'][0].cat_id
        return context
 
    def get_queryset(self):
        return Goods.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)