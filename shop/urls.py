from django.contrib import admin
from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', ShopHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('catalog/', catalog, name='catalog'),
    path('article/', ShowArticle.as_view(), name='article'),
    path('login/', RegisterUser.as_view(), name='login'),
    path('auth/', LoginUser.as_view(), name='auth'),
    path('logout/', logout_user, name='logout'),
    path('cart/', Cart, name='cart'),
    path('catalog/<slug:post_slug>/', ShowGoods.as_view(), name='post'),
    path('category/<slug:cat_slug>/', GoodsCategory.as_view(), name='category'),
    path('cats/<int:catid>/', categories),
]