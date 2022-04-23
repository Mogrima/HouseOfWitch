from django.conf import settings

from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
import operator
from .utils.upload import upload_function

User = get_user_model()

class Goods(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название товара')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    price = models.FloatField(verbose_name='Цена')
    description = models.TextField(blank=True, verbose_name="Описание товара")
    photo = models.ImageField(upload_to=upload_function, blank=True, verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Показано на сайте')
    stock = models.IntegerField(default=1, verbose_name='Наличие на складе')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    @property
    def ct_model(self):
        return self._meta.model_name

    @property
    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return "../static/shop/img/notavailable2.jpg"
    class Meta:
        verbose_name = 'Товары'
        verbose_name_plural = 'Товары'
        ordering = ['time_create', 'title']

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
 
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="imgarticle/%Y/", blank=True, verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано на сайте')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', kwargs={'article_slug': self.slug})

    class Meta:
        verbose_name = 'Статью'
        verbose_name_plural = 'Статьи'
        ordering = ['time_create', 'title']

class CartGoods(models.Model):

    MODEL_CARTPRODUCT_DISPLAY_NAME_MAP = {
        "Goods": {"is_constructable": True, "fields": ["title"], "separator": ' - '}
    }

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.PROTECT)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.PROTECT, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    final_price = models.FloatField(verbose_name='Итоговая цена')
    qty = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f"Продукт: {self.content_object} (для корзины)"

    @property
    def display_name(self):
        model_fields = self.MODEL_CARTPRODUCT_DISPLAY_NAME_MAP.get(self.content_object.__class__._meta.model_name.capitalize())
        if model_fields and model_fields['is_constructable']:
            display_name = model_fields['separator'].join(
                [operator.attrgetter(field)(self.content_object) for field in model_fields['fields']]
            )
            return display_name
        if model_fields and not model_fields['is_constructable']:
            display_name = operator.attrgetter(model_fields['field'])(self.content_object)
            return display_name

        return self.content_object

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Продукт корзины'
        verbose_name_plural = 'Продукты корзины'

class Cart(models.Model):

    owner = models.ForeignKey('Customer', blank=True, verbose_name='Владелец', on_delete=models.PROTECT)
    products = models.ManyToManyField(CartGoods, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0, verbose_name='Общее кол-во товаров')
    final_price = models.FloatField(default=0, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False, verbose_name='В заказе')
    for_anonymous_user = models.BooleanField(default=False, verbose_name='Неавторизованный пользователь')

    def products_in_cart(self):
        return [c.content_object for c in self.products.all()]

    def __str__(self):
        return f"Корзина: id - {str(self.id)} {self.owner}"

    class Meta:
        verbose_name = 'Корзина покупателя'
        verbose_name_plural = 'Корзины покупателей'
        ordering = ['owner',]

class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELED = 'canceled'

    BUYING_TYPE_RF = 'pochta'
    BUYING_TYPE_DELIVERY = 'SDEK'

    PAY_FALSE = 'Неоплачен'
    PAY_PROGRESS = 'Платеж в обработке'
    PAY_TRUE = 'Оплачен'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ отдан'),
        (STATUS_CANCELED, 'Заказ отменен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_RF, 'Почта РФ'),
        (BUYING_TYPE_DELIVERY, 'СДЭК')
    )

    STATUS_PAY_CHOICES = (
        (PAY_FALSE, 'Неоплачен'),
        (PAY_PROGRESS, 'Платеж в обработке'),
        (PAY_TRUE, 'Оплачен'),
    )

    customer = models.ForeignKey(
        'Customer', on_delete=models.CASCADE, related_name='orders', default='', verbose_name='Покупатель'
        )
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    surname = models.CharField(max_length=255, blank=True, default='', verbose_name='Отчество (если есть)')
    email = models.EmailField(max_length = 254, default='', verbose_name='Электронная почта')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True, default='', verbose_name='Корзина')
    buying_type = models.CharField(max_length=100, choices=BUYING_TYPE_CHOICES, default=BUYING_TYPE_RF, verbose_name='Тип заказа',)
    state = models.CharField(max_length=255, verbose_name='Область/Край')
    city = models.CharField(max_length=255, verbose_name='Город')
    street = models.CharField(max_length=1024, verbose_name='Улица')
    house = models.CharField(max_length=30, verbose_name='Дом')
    flat = models.CharField(max_length=30, blank=True, verbose_name='Квартира')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_NEW, verbose_name='Статус заказа')
    pay_status = models.CharField(max_length=100, choices=STATUS_PAY_CHOICES, default=PAY_FALSE, verbose_name='Статус платежа')
    comment = models.TextField(blank=True, max_length=255, verbose_name='Комментарий к заказу')
    created_at = models.DateField(verbose_name='Дата создания заказа', auto_now=True)

    def __str__(self):
         return f"Заказ: № - {str(self.id)}, владельца {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class Customer(models.Model):
    """Покупатель"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    in_active = models.BooleanField(default=True, verbose_name='Активный')
    customer_orders = models.ManyToManyField(
        Order, blank=True, related_name='related_customer', verbose_name='Заказы покупателя'
    )
    wishlist = models.ManyToManyField(Goods, blank=True, verbose_name='Список ожидаемого')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    email = models.EmailField(max_length = 254, default='', verbose_name='Email')
    adress = models.TextField(blank=True, verbose_name='Адрес')

    def __str__(self):
        return f"{self.user.username}"


    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
        ordering = ['user',]

class Notification(models.Model):

    recipient = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Получатель')
    text = models.TextField(verbose_name='Текст')
    read = models.BooleanField(default=False, verbose_name='Прочитано')

    def __str__(self):
        return f"Уведомление для {self.recipient.user.username} | id={self.id}"

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
