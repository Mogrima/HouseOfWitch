from django.contrib import admin
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from PIL import Image

from .models import *

class GoodsAdminForm(ModelForm):

    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (1200, 1200)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].help_text = mark_safe('<strong style="color:yellow;">Загружайте изображение с минимальным разрешением {}x{}</strong>'.format(
            *self.MIN_RESOLUTION
        ))

class GoodsAdmin(admin.ModelAdmin):
    form = GoodsAdminForm
    list_display = ('id', 'title', 'stock', 'price', 'time_create', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title", )}

admin.site.register(Goods, GoodsAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name", )}

admin.site.register(Category, CategoryAdmin)

class  ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ("title", )}

admin.site.register(Article,  ArticleAdmin)

class OrderInline(admin.TabularInline):
    model = Order
    fields = ("id", "first_name", "last_name", "status", "pay_status")
    extra = 1

class  CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_display_links = ('id', 'user')
    fields = ("user", "in_active", "wishlist", "phone", "email", "adress")
    filter_horizontal = ('wishlist',)
    inlines = (OrderInline,)
    search_fields = ('user', 'address')

admin.site.register(Customer,  CustomerAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner')
    list_display_links = ('id', 'owner')
    search_fields = ('owner',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'first_name', 'last_name', 'created_at', 'status')

admin.site.register(Cart, CartAdmin)
admin.site.register(Order,  OrderAdmin)
admin.site.register(Notification)
admin.site.register(CartGoods)