from django.db.models import Count
from django.http import request

from .models import *


menu = [{'title': "Главная", 'url_name': 'home', 'url_link': '/'},
		{'title': "Каталог", 'url_name': 'catalog', 'url_link': 'catalog'},
        {'title': "О нас", 'url_name': 'about', 'url_link': 'about'},
        {'title': "Статьи", 'url_name': 'article', 'url_link': 'article'},

        ]

class DataMixin:
	paginate_by = 6
	def get_user_context(self, **kwargs):
		context = kwargs
		cats = Category.objects.annotate(Count('goods'))
		
		context['menu'] = menu

		context['cats'] = cats
		if 'cat_selected' not in context:
			context['cat_selected'] = 0
  	
		return context