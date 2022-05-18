from django.db import models

def recalc_cart(cart):
  cart_data = cart.products.aggregate(models.Sum('final_price'), models.Count('id'))
  if cart_data.get('final_price__sum'):
    cart.final_price = cart_data['final_price__sum']
  else:
    cart.final_price = 0
  cart.total_products = cart_data['id__count']
  cart.save()

def recalc_count(cart):
  total_count = 0
  if cart == None:
    total_count = 0
    return total_count
  else:
    for item in cart.products.all():
      total_count = total_count +  item.qty
    return  total_count