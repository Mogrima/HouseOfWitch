from django.contrib import admin

from .models import *

class GoodsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
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

class  CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_display_links = ('id', 'user')
    search_fields = ('user', 'address')

admin.site.register(Customer,  CustomerAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner')
    list_display_links = ('id', 'owner')
    search_fields = ('owner',)

admin.site.register(Cart, CartAdmin)