from django.conf import settings

from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from PIL import Image

User = get_user_model()

class Goods(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название товара')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    price = models.FloatField(verbose_name='Цена')
    description = models.TextField(blank=True, verbose_name="Описание товара")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default='0')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def save(self):
        if self.photo:
            super().save()
            img = Image.open(self.photo.path)

            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.photo.path)

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
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', kwargs={'article_slug': self.slug})

    class Meta:
        verbose_name = 'Статью'
        verbose_name_plural = 'Статьи'
        ordering = ['time_create', 'title']

class CartGoods(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.PROTECT)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.PROTECT, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    final_price = models.FloatField(verbose_name='Итоговая цена')
    qty = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.content_object.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Продукт корзины'
        verbose_name_plural = 'Продукты корзины'

class Cart(models.Model):

    owner = models.ForeignKey('Customer', blank=True, verbose_name='Владелец', on_delete=models.PROTECT)
    products = models.ManyToManyField(CartGoods, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.FloatField(default=0, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Корзина покупателя'
        verbose_name_plural = 'Корзины покупателей'
        ordering = ['owner',]

class Order(models.Model):
    pass
class Customer(models.Model):
    """Покупатель"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    in_active = models.BooleanField(default=True, verbose_name='Активный')
    customer_orders = models.ManyToManyField(
        Order, blank=True, related_name='related_customer', verbose_name='Заказы покупателя'
    )
    wishlist = models.ManyToManyField(Goods, blank=True, verbose_name='Список ожидаемого')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    adress = models.TextField(blank=True, verbose_name='Адрес')

    def __str__(self):
        return f"{self.user.username}"


    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
        ordering = ['user',]

