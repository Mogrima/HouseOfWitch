from django.contrib import admin
from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', ShopHome.as_view(), name='home'),
    path('about/', about.as_view(), name='about'),
    path('catalog/', catalog.as_view(), name='catalog'),
    path('article/', ShowArticle.as_view(), name='article'),
    path('article/<slug:article_slug>/', Article.as_view(), name='article_content'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('account/', AccountView.as_view(), name='account'),
    # path('cart/', Cart, name='cart'),
    path('goods/<slug:post_slug>/', ShowGoods.as_view(), name='post'),
    path('category/<slug:cat_slug>/', GoodsCategory.as_view(), name='category'),
    path('cats/<int:catid>/', categories),

    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:ct_model>/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-qty/<str:ct_model>/<str:slug>/', ChangeQTVView.as_view(), name='change_qty'),
    path('change_up/<str:ct_model>/<str:slug>/', ChangeUpCart.as_view(), name='change_up'),
    path('change_down/<str:ct_model>/<str:slug>/', ChangeDownCart.as_view(), name='change_down'),
    path('add-to-wishlist/<int:post_id>/', AddToWishlist.as_view(), name='add_to_wishlist'),
    path('remove-from-wishlist/<int:post_id>/', RemoveFromWishListView.as_view(), name='remove_from_wishlist'),
    path('make-order/', MakeOrderView.as_view(), name='make-order'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),

    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('policy/', PolicyView.as_view(), name='policy'),
]