from django.db.models import Count

from .models import *


menu = [{'title': "Главная", 'url_name': 'home'},
        {'title': "О нас", 'url_name': 'about'},
        {'title': "Статьи", 'url_name': 'article'},

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
