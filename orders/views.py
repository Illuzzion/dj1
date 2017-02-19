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

    def get_queryset(self):
        city_name = self.kwargs['city_slug']
        return Shop.objects.filter(city__slug=city_name)


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
    return HttpResponse("add shop")
    # request.POST['city'] = city
    #
    # form = ShopForm(request.POST or None)
    #
    # if form.is_valid():
    #     form.save()
    #     return redirect('orders:city_list')
    # else:
    #     return render(request, 'orders/add_shop.html', dict(form=form))
