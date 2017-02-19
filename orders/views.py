from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic

from orders.forms import CityForm, ShopForm
from .models import Order, Shop, City


class IndexView(generic.ListView):
    model = Order
    template_name = 'orders/index.html'


# order = Order.objects.get(id=1)
# shops = Shop.objects.filter(order=order)

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'orders/detail.html'


class CityListView(generic.ListView):
    model = City
    template_name = 'orders/city_list.html'


class ShopListView(generic.ListView):
    model = Shop
    template_name = 'orders/shop_list.html'
    context_object_name = 'data'

    def get_queryset(self):
        city = get_object_or_404(City, slug=self.kwargs['city_slug'])
        shops = Shop.objects.filter(city=city)
        return locals()
        # return dict(shops=shop_list, city=city)


def add_city(request):
    form = CityForm(request.POST or None)

    if form.is_valid():
        form.save()

        # http://djbook.ru/rel1.8/topics/http/shortcuts.html#redirect
        return redirect('orders:city_list')
    else:
        return render(request, 'orders/add_city.html', dict(form=form))


def add_shop(request, city_slug):
    city = get_object_or_404(City, slug=city_slug)
    # TODO: копать тут

    form = ShopForm(request.POST or None)
    #
    if form.is_valid():
        pass
    # form.save()
    #     return redirect('orders:city_list')
    else:
        form.current_city = city
        return render(request, 'orders/add_shop.html', dict(form=form))
