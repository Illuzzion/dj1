from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from orders.forms import CityForm
from .models import Order, Shop, City


class IndexView(generic.ListView):
    model = Order
    template_name = 'orders/index.html'


# order = Order.objects.get(id=1)
# shops = Shop.objects.filter(order=order)

class DetailView(generic.DetailView):
    model = Order
    template_name = 'orders/detail.html'


class CityListView(generic.ListView):
    model = City
    template_name = 'orders/city_list.html'


class ShopListView(generic.ListView):
    model = Shop
    template_name = 'orders/shop_list.html'

    def get_queryset(self):
        city_name = self.kwargs['city_name']
        return Shop.objects.filter(city__slug=city_name)


def add_city(request):
    form = CityForm(request.POST or None)

    if form.is_valid():
        form.save()

        # http://djbook.ru/rel1.8/topics/http/shortcuts.html#redirect
        return redirect('orders:city_list')
    else:
        return render(request, 'orders/add_city.html', dict(form=form))
