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
from .utils.recalc_cart import recalc_cart, recalc_count
from .utils.users import *
from django.views import View
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from json import dumps
from django.core.mail import send_mail
from django.template.loader import get_template

import json

from django.http import HttpResponseBadRequest, JsonResponse
from django.db.models import Q

from .forms import *
from .models import *
from .mixins import *


class ShopHome(DataMixin, ListView):
    model = Goods
    template_name = 'shop/index.html'
    context_object_name = 'posts'




    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        total_count = recalc_count(self.cart)
        context['title'] = 'Главная страница'
        context['menu'] = self.menu
        context['desc'] = 'Заходите на кружку ароматного чая к Лесной Ведьмы. Она приготовила для вас нечто особенное. Добро пожаловать в магазин магической атрибутики.'
        context['cats'] = self.cats
        context['cart'] = self.cart
        context['total_count'] = total_count
        return context

class about(DataMixin, views.View):
  def get(self, request, *args, **kwargs):
    # dataDictionary = {
    #     'hello': 'World',
    #     'geeks': 'forgeeks',
    #     'ABC': 123,
    #     456: 'abc',
    #     14000605: 1,
    #     'list': ['geeks', 4, 'geeks'],
    #     'dictionary': {'you': 'can', 'send': 'anything', 3: 1}
    #     }
    # dump data
    # dataJSON = dumps(dataDictionary)
    total_count = recalc_count(self.cart)
    context = {
      'title': 'О нас',
      'menu': self.menu,
      'cart': self.cart,
      'total_count': total_count,
      'desc': 'Раздел информации о Лесной Ведьмe и ее работе. Заходите на досуге почитать.',
    #   'data': dataJSON
    }
    return render(request, 'shop/about.html', context)


# def catalog(request):
#     return render(request, 'shop/catalog.html', {'menu': menu, 'title': 'Каталог'})

class catalog(DataMixin, ListView):
    model = Goods
    template_name = 'shop/catalog.html'
    context_object_name = 'posts'
        
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        total_count = recalc_count(self.cart)
        context['title'] = 'Каталог'
        context['menu'] = self.menu
        context['cats'] = self.cats
        context['cart'] = self.cart
        context['total_count'] = total_count
        context['desc'] = 'Ведьма тщательно и бережно подбирает магические товары для вас. В этом каталоге представлены магические предметы для любого вида колдовства.'
        return context


def categories(request, catid):
    return HttpResponse(f"<h1>Товары по категориям</h1><p>{catid}</p>")


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена.</h1>")


class ShowArticle(DataMixin, ListView):
    model = Article
    template_name = 'shop/articles.html'
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        total_count = recalc_count(self.cart)
        context['title'] = 'Статьи'
        context['menu'] = self.menu
        context['cats'] = self.cats
        context['cart'] = self.cart
        context['total_count'] = total_count
        context['desc'] = 'В этом разделе собраны все знания и опыт Лесной Ведьмы, скурпулёзно собранные ей для вас. Статьи про магические обряды и правила их проведения.'
        return context

class Article(DataMixin, DetailView):
    model = Article
    template_name = 'shop/article.html'
    slug_url_kwarg = 'article_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        total_count = recalc_count(self.cart)
        context['title'] = context['post']
        context['menu'] = self.menu
        context['cats'] = self.cats
        context['cart'] = self.cart
        context['total_count'] = total_count
        return context

class ShowGoods(DataMixin, DetailView):
    model = Goods
    template_name = 'shop/goods.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        total_count = recalc_count(self.cart)
        context['title'] = context['post']
        context['menu'] = self.menu
        context['cats'] = self.cats
        context['cart'] = self.cart
        context['total_count'] = total_count
        context['posts'] = Goods.objects.all()[:5]
        return context


class GoodsCategory(DataMixin, ListView):
    model = Goods
    template_name = 'shop/catalog.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        total_count = recalc_count(self.cart)
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['menu'] = self.menu
        context['cats'] = self.cats
        context['cat_selected'] = context['posts'][0].cat_id
        context['cart'] = self.cart
        context['total_count'] = total_count
        context['desc'] = 'Товары из категории ' + str(context['posts'][0].cat)
        return context

    def get_queryset(self):
        return Goods.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

# class CartView(DataMixin, views.View):
#   def get(self, request, *args, **kwargs):
#     return render(request, 'shop/cart.html', {"cart": self.cart})

class CartView(DataMixin, ListView):
    def get(self, request, *args, **kwargs):
        total_count = recalc_count(self.cart)
        form = OrderForm(request.POST or None)
        context = {
            'form': form,
            'cart': self.cart,
            'total_count': total_count,
            'menu': self.menu,
            'title': 'Корзина',
            'desc': 'Ваша корзина'
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
    # if created:
    #     self.cart.products.add(cart_product)
    #     recalc_cart(self.cart)
    #     return HttpResponseRedirect(request.META['HTTP_REFERER'])
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'GET':
            self.cart.products.add(cart_product)
            recalc_cart(self.cart)
            messages.add_message(request, messages.INFO, "Количество изменено")
            return JsonResponse({'context': 'created'})
    else:
        if created:
            self.cart.products.add(cart_product)
            recalc_cart(self.cart)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    # else:
    #     return HttpResponseRedirect(request.META['HTTP_REFERER'])
    

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

class ChangeUpCart(DataMixin, views.View):
   def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product, created = CartGoods.objects.get_or_create(
        user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            if request.method == 'GET':
                cart_product.qty += 1
                cart_product.save()
                recalc_cart(self.cart)
                return JsonResponse({'context': 'succes'})
        else:
            cart_product.qty += 1
            cart_product.save()
            recalc_cart(self.cart)
            messages.add_message(request, messages.INFO, "Количество изменено")
            return HttpResponseRedirect(request.META['HTTP_REFERER'])

class ChangeDownCart(DataMixin, views.View):
   def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product, created = CartGoods.objects.get_or_create(
        user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            if request.method == 'GET':
                cart_product.qty -= 1
                cart_product.save()
                recalc_cart(self.cart)
                return JsonResponse({'context': 'succes'})
        else:
            cart_product.qty -= 1
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
        if request.user.is_authenticated:
            return redirect('account')
        form = RegisterUserForm(request.POST or None)
        title = 'Регистрация'
        context = {
        'form': form,
        'menu': self.menu,
        'cats': self.cats,
        'title': title,
        'desc': 'На этой странице Ведьма получает информацию о вас в свою картотеку. Благодаря регистрации вы сможете отслеживать свои заказы, а также добавлять товары в список ожидаемого.'
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

            send_email_for_verify(request, user)

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
class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        

        # if user is not None and token_generator.check_token(user, token):
            
        login(request, user)
        customer = Customer.objects.get(user=request.user)
        customer.in_active = True
        customer.save()
        return redirect('home')
        # return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user
class LoginUser(DataMixin, views.View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('account')
        form = LoginUserForm(request.POST or None)
        title = 'Авторизация'
        context = {
            'form': form,
            'menu': self.menu,
            'cats': self.cats,
            'title': title,
            'desc': 'Подтвердите свою личность Ведьме на этой странице, чтобы получить доступ к отслеживанию товаров и списка листа ожидаемого.'
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
                return redirect('home')
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
    if not request.user.is_authenticated:
        return redirect('login')
    customer = Customer.objects.get(user=request.user)
    total_count = recalc_count(self.cart)
    context = {
      'customer': customer,
      'title': 'Личный кабинет ' + request.user.username,
      'menu': self.menu,
      'cart': self.cart,
      'total_count': total_count,
      'desc': 'Это ваш личный кабинет в магазине Лесной Ведьмы. Тут вы можете отслеживать свои заказы и лист ожидания.'
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
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.state = form.cleaned_data['state']
            new_order.city = form.cleaned_data['city']
            new_order.street = form.cleaned_data['street']
            new_order.house = form.cleaned_data['house']
            new_order.flat = form.cleaned_data['flat']
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
            subject = 'Ваш заказ оформлен!'
            send_text = 'Вы оформили заказ на сайте интернет-магазина Дом Лесной Ведьмы'
            order = customer.orders.last()
            context = {
                'order': order,
            }
            send_mail(
            'Ваш заказ оформлен!',
            'Ваш заказ оформлен!',
            'mushroom@houseofwitch.ru',
            [form.cleaned_data['email']],
            fail_silently=True,
            html_message=get_template('shop/mail/checkout_mail.html').render(context)
            )
            return HttpResponseRedirect('/checkout/')
        return HttpResponseRedirect('/cart/')

class CheckoutView(DataMixin, views.View):
  def get(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')
    customer = Customer.objects.get(user=request.user)
    order = customer.orders.last()
    if (order):
        context = {
        'order': order,
        'title': 'Заказ оформлен!',
        'menu': self.menu,
        'cart': self.cart,
        'desc': 'Ваш заказ оформлен!'
        }
        return render(request, 'shop/checkout.html', context)

    else:
        return redirect('catalog')

class SearchResultsView(DataMixin, ListView):
    model = Goods
    template_name = 'shop/catalog.html'
    context_object_name = 'posts'

    def get_queryset(self): # новый
        query = self.request.GET.get('q')
        object_list = Goods.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        return object_list
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        total_count = recalc_count(self.cart)
        context['title'] = 'Поиск'
        context['menu'] = self.menu
        context['cats'] = self.cats
        context['cart'] = self.cart
        context['total_count'] = total_count
        context['desc'] = 'Страница, на которую выводятся результаты вашего поискового запроса.'
        context['count'] = self.object_list.count
        return context
class PolicyView(DataMixin, views.View):
  def get(self, request, *args, **kwargs):
    total_count = recalc_count(self.cart)
    context = {
      'title': 'Политика конфидициальности',
      'menu': self.menu,
      'cart': self.cart,
      'total_count': total_count,
      'desc': 'Страница политики конфидициальности интернет-магазина Дом Лесной Ведьмы.'
    }
    return render(request, 'shop/policy.html', context)

class DeliveryView(DataMixin, views.View):
  def get(self, request, *args, **kwargs):
    total_count = recalc_count(self.cart)
    context = {
      'title': 'Доставка и оплата',
      'menu': self.menu,
      'cart': self.cart,
      'total_count': total_count,
      'desc': 'Информация об оплате и доставке интернет-магазина Дом Лесной Ведьмы.'
    }
    return render(request, 'shop/delivery.html', context)