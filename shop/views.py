from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpRequest
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
from .utils.recalc_cart import recalc_cart
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from .forms import *
from .models import *
from .mixins import *


class ShopHome(DataMixin, ListView):
    model = Goods
    template_name = 'shop/index.html'
    context_object_name = 'posts'
        
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = self.menu
        context['cats'] = self.cats
        context['cart'] = self.cart
        return context

class about(DataMixin, views.View):
  def get(self, request, *args, **kwargs):
    context = {
      'title': 'О нас',
      'menu': self.menu,
      'cart': self.cart
    }
    return render(request, 'shop/about.html', context)


# def catalog(request):
#     return render(request, 'shop/catalog.html', {'menu': menu, 'title': 'Каталог'})

class catalog(DataMixin, ListView):
    model = Goods
    template_name = 'shop/index.html'
    context_object_name = 'posts'
        
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['menu'] = self.menu
        context['cats'] = self.cats
        context['cart'] = self.cart
        return context


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
        context['title'] = 'Статьи'
        context['menu'] = self.menu
        context['cats'] = self.cats
        return context

class ShowGoods(DataMixin, DetailView):
    model = Goods
    template_name = 'shop/goods.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = self.menu
        context['cats'] = self.cats
        return context


class GoodsCategory(DataMixin, ListView):
    model = Goods
    template_name = 'shop/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['menu'] = self.menu
        context['cats'] = self.cats
        context['cat_selected'] = context['posts'][0].cat_id
        return context

    def get_queryset(self):
        return Goods.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

# class CartView(DataMixin, views.View):
#   def get(self, request, *args, **kwargs):
#     return render(request, 'shop/cart.html', {"cart": self.cart})

class CartView(DataMixin, ListView):
    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        context = {
            'form': form,
            'cart': self.cart,
            'menu': self.menu,
            'title': 'Корзина'
        }
        return render(request, 'shop/cart.html', context)


class AddToCartView(DataMixin, views.View):
  def get(self, request, *args, **kwargs):
    ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
    content_type = ContentType.objects.get(model=ct_model)
    product = content_type.model_class().objects.get(slug=product_slug)
    cart_product, created = CartGoods.objects.get_or_create(
      user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
    )
    if created:
      self.cart.products.add(cart_product)
    recalc_cart(self.cart)
    messages.add_message(request, messages.INFO, "Товар добавлен в корзину")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

class DeleteFromCartView(DataMixin, views.View):
  def get(self, request, *args, **kwargs):
    ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
    content_type = ContentType.objects.get(model=ct_model)
    product = content_type.model_class().objects.get(slug=product_slug)
    cart_product = CartGoods.objects.get(
      user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
    )
    self.cart.products.remove(cart_product)
    cart_product.delete()
    recalc_cart(self.cart)
    messages.add_message(request, messages.INFO, "Товар удален")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

class ChangeQTVView(DataMixin, views.View):
  def post(self, request, *args, **kwargs):
    ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
    content_type = ContentType.objects.get(model=ct_model)
    product = content_type.model_class().objects.get(slug=product_slug)
    cart_product = CartGoods.objects.get(
      user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
    )
    qty = int(request.POST.get('qty'))
    cart_product.qty = qty
    cart_product.save()
    recalc_cart(self.cart)
    messages.add_message(request, messages.INFO, "Количество изменено")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

class AddToWishlist(views.View):

    @staticmethod
    def get(request, *args, **kwargs):
        goods = Goods.objects.get(id=kwargs['post_id'])
        customer = Customer.objects.get(user=request.user)
        customer.wishlist.add(goods)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

class RemoveFromWishListView(views.View):

    @staticmethod
    def get(request, *args, **kwargs):
        goods = Goods.objects.get(id=kwargs['post_id'])
        customer = Customer.objects.get(user=request.user)
        customer.wishlist.remove(goods)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

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
            # new_user.first_name = form.cleaned_data['first_name']
            # new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            # Сохранить пароль можно только у уже сохраненного пользователя
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                email=form.cleaned_data['email'],
                # adress=form.cleaned_data['address']
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

class AccountView(DataMixin, views.View):
  def get(self, request, *args, **kwargs):
    customer = Customer.objects.get(user=request.user)
    context = {
      'customer': customer,
      'title': 'Личный кабинет ' + request.user.username,
      'menu': self.menu,
      'cart': self.cart
    }
    return render(request, 'shop/account.html', context)
class MakeOrderView(DataMixin, views.View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            out_of_stock = []
            more_than_on_stock = []
            out_of_stock_message = ""
            more_than_on_stock_message = ""
            for item in self.cart.products.all():
                if not item.content_object.stock:
                    out_of_stock.append(' - '.join([
                        item.content_object.title
                    ]))
                if item.content_object.stock and item.content_object.stock < item.qty:
                    more_than_on_stock.append(
                        {'product': ' - '.join([item.content_object.title]),
                         'stock': item.content_object.stock, 'qty': item.qty}
                    )
            if out_of_stock:
                out_of_stock_products = ', '.join(out_of_stock)
                out_of_stock_message = f'Товара уже нет в наличии: {out_of_stock_products}. \n'

            if more_than_on_stock:
                for item in more_than_on_stock:
                    more_than_on_stock_message += f'Товар: {item["product"]}. ' \
                                                  f'В наличии: {item["stock"]}. ' \
                                                  f'Заказано: {item["qty"]}\n'
            error_message_for_customer = ""
            if out_of_stock:
                error_message_for_customer = out_of_stock_message + '\n'
            if more_than_on_stock_message:
                error_message_for_customer += more_than_on_stock_message + '\n'

            if error_message_for_customer:
                messages.add_message(request, messages.INFO, error_message_for_customer)
                return HttpResponseRedirect('/cart/')

            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.email = form.cleaned_data['email']
            new_order.surname = form.cleaned_data['surname']
            new_order.phone = form.cleaned_data['phone']
            new_order.adress = form.cleaned_data['adress']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()

            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)

            for item in self.cart.products.all():
                item.content_object.stock -= item.qty
                item.content_object.save()

            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с Вами свяжется')
            return HttpResponseRedirect('/account/')
        return HttpResponseRedirect('/cart/')