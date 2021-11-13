from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.core.paginator import Paginator
from django import views
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

from .forms import *
from .models import *
from .utils import *


class ShopHome(DataMixin, ListView):
    model = Goods
    template_name = 'shop/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Goods.objects.filter(is_published=True).order_by('-id')[:9]


def about(request):
    return render(request, 'shop/about.html', {'menu': menu, 'title': 'О нас'})


def catalog(request):
    return render(request, 'shop/catalog.html', {'menu': menu, 'title': 'Каталог'})


def categories(request, catid):
    return HttpResponse(f"<h1>Товары по категориям</h1><p>{catid}</p>")


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена.</h1>")


class ShowArticle(DataMixin, ListView):
    model = Article
    template_name = 'shop/article.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Статьи")
        context = dict(list(context.items()) + list(c_def.items()))
        return context


def Cart(request):
    return render(request, 'shop/cart.html', {'menu': menu, 'title': 'Содержимое корзинки'})


class ShowGoods(DataMixin, DetailView):
    model = Goods
    template_name = 'shop/goods.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class GoodsCategory(DataMixin, ListView):
    model = Goods
    template_name = 'shop/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Goods.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

class RegisterUser(DataMixin, views.View):

    def get(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST or None)
        title = 'Регистрация'
        context = {
        'form': form,
        'menu': self.menu,
        'cats': self.cats,
        'title': title
        }
        return render(request, 'shop/registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            # Сохранить пароль можно только у уже сохраненного пользователя
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                adress=form.cleaned_data['address']
            )
            user = authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        title = 'Регистрация'
        context = {
        'form': form,
        'menu': self.menu,
        'cats': self.cats,
        'title': title
        }
        return render(request, 'shop/registration.html', context)


class LoginUser(DataMixin, views.View):

    def get(self, request, *args, **kwargs):
        form = LoginUserForm(request.POST or None)
        title = 'Авторизация'
        context = {
            'form': form,
            'menu': self.menu,
            'cats': self.cats,
            'title': title
        }

        return render(request, 'shop/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginUserForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        title = 'Авторизация'
        context = {
            'form': form,
            'menu': self.menu,
            'cats': self.cats,
            'title': title
        }
        return render(request, 'shop/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')