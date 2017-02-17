from django.shortcuts import render
from django.views import generic

from .models import Order, Shop


class IndexView(generic.ListView):
    model = Order
    template_name = 'orders/index.html'


# order = Order.objects.get(id=1)
# shops = Shop.objects.filter(order=order)

class DetailView(generic.DetailView):
    model = Order
    template_name = 'orders/detail.html'
