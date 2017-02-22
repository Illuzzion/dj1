from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic

from .forms import CityForm, ShopForm, ShopFormCBV
from .models import Order, Shop, City, OrderEntry


class OrderIndexView(generic.ListView):
    # отсортируем по id через queryset
    queryset = Order.objects.order_by('-id')
    template_name = 'orders/index.html'
    # paginate_by = 10


class OrderDetailView(generic.ListView):
    template_name = 'orders/order_details.html'

    def get_queryset(self):
        order = Order.objects.get(pk=self.kwargs['pk'])
        order_entries = OrderEntry.objects.filter(order=order)
        return locals()


class CityListView(generic.ListView):
    model = City
    template_name = 'orders/city_list.html'
    # paginate_by = 5


class ShopListView(generic.ListView):
    """
    Выводим список магазинов
    """
    template_name = 'orders/shop_list.html'

    def get_context_data(self, **kwargs):
        """
        добавиим в контекст, передаваемый в шаблон, данные
        :param kwargs:
        :return:
        """
        context = super(ShopListView, self).get_context_data(**kwargs)
        # в контексте уже есть список магазинов с городами, возьмем первый
        context['city'] = context['shop_list'][0].city
        return context

    def get_queryset(self):
        city = get_object_or_404(City, slug=self.kwargs['city_slug'])
        return Shop.objects.filter(city=city)


# используем CreateView
class CityFormView(generic.CreateView):
    form_class = CityForm
    template_name = 'orders/add_city.html'

    # так не хочет работать, но работает с указанием ссылки - '/orders/city/'
    # success_url = reverse('orders:city_list')

    def get_success_url(self):
        return reverse('orders:city_list')


# def add_city(request):
#     """
#     Добавление города
#     :param request:
#     :return:
#     """
#     form = CityForm(request.POST or None)
#
#     if form.is_valid():
#         form.save()
#
#         # http://djbook.ru/rel1.8/topics/http/shortcuts.html#redirect
#         return redirect('orders:city_list')
#     else:
#         return render(request, 'orders/add_city.html', dict(form=form))


class ShopFormView(generic.CreateView):
    form_class = ShopFormCBV
    template_name = 'orders/add_shopcbv.html'

    def get(self, request, *args, **kwargs):
        city = get_object_or_404(City, slug=self.kwargs['city_slug'])
        form = self.form_class(initial={'city': city})
        return render(request, self.template_name, locals())
        # для пояснения хода мыслей
        # return render(request, self.template_name, {'form': form, 'city': city})
        # return render(request, self.template_name, {'form': form, 'city_slug': self.kwargs['city_slug']})

    def get_success_url(self):
        return reverse('orders:shop_list', kwargs=self.kwargs)
        # для наглядности
        # return reverse('orders:shop_list', kwargs={'city_slug': self.kwargs['city_slug']})

        # добавим в контекст шаблона слаг текущего города
        # def get_context_data(self, **kwargs):
        #     context = super(ShopFormView, self).get_context_data(**kwargs)
        #     context['city_slug'] = self.kwargs['city_slug']
        #     return context


def add_shop(request, city_slug):
    """
    Добавление магазина
    :param request: реквест
    :param city_slug: слаг города из строки запроса
    :return:
    """
    city = get_object_or_404(City, slug=city_slug)

    form = ShopForm(request.POST or None)

    if form.is_valid():
        # форму нужно сохранить в другую переменную, которую можно изменять
        shop = form.save(commit=False)
        shop.city = city
        shop.save()
        return redirect('orders:shop_list', city_slug=city.slug)
    else:
        form.current_city = city
        return render(request, 'orders/add_shop.html', dict(form=form))
