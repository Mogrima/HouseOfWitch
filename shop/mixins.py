from django.db.models import Count
from django.http import request

from .models import *

class DataMixin:
	paginate_by = 6
	menu = [
		{'title': "Главная", 'url_name': 'home', 'url_link': '/'},
		{'title': "Каталог", 'url_name': 'catalog', 'url_link': 'catalog'},
        {'title': "О нас", 'url_name': 'about', 'url_link': 'about'},
        {'title': "Статьи", 'url_name': 'article', 'url_link': 'article'},

        ]
	cats = Category.objects.annotate(Count('goods'))

	def dispatch(self, request, *args, **kwargs):
		cart = None
		if request.user.is_authenticated:
			customer = Customer.objects.filter(user=request.user).first()
		# если покупатель не найден, связанные с пользователем, тогда создаем его
			if not customer:
				customer = Customer.objects.create(
				user = request.user
				)
			cart = Cart.objects.filter(owner=customer, in_order=False).first()
		#
			if not cart:
				cart = Cart.objects.create(owner=customer)
			
		# else:
		# 	cart = Cart.objects.filter(for_anonymous_user=True).first()
		# 	if not cart:
		# 		cart = Cart.objects.create(for_anonymous_user=True)
		self.cart = cart
		return super().dispatch(request, *args, **kwargs)

	def get_user_context(self, **kwargs):
		context = kwargs
		cats = Category.objects.annotate(Count('goods'))
		
		context['menu'] = self.menu

		context['cats'] = cats
		if 'cat_selected' not in context:
			context['cat_selected'] = 0
  	
		return context

