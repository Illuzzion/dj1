from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .forms import CityForm, ShopFormCBV, OrderEntryForm, OrderCreateForm
from .models import Order, Shop, City, OrderEntry


class OrderIndexView(generic.ListView):
    # отсортируем по id через queryset
    queryset = Order.objects.order_by('-id')
    template_name = 'orders/index.html'


class OrderCreateView(generic.CreateView):
    form_class = OrderCreateForm
    template_name = 'orders/new_order.html'

    def get_success_url(self):
        """
        при удачном добавлении, перенаправим на форму только что добавленного объекта
        :return:
        """
        return reverse('orders:order_details', kwargs={'pk': self.object.id})
        # return reverse('orders:order_details', args=(self.object.id,))
        # так тоже работает


class OrderDetailView(generic.ListView, generic.CreateView):
    form_class = OrderEntryForm

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        order_entries = OrderEntry.objects.filter(order=order)
        form = self.form_class(initial={'order': order})
        return self.render_to_response(locals())

    def get_success_url(self):
        return reverse('orders:order_details', kwargs=self.kwargs)

    def get_template_names(self):
        """
        если есть GET параметр print, то вернем форму для печати
        иначе, обычную форму для заполнения
        :return:
        """
        return ['orders/print_order_details.html'] if self.request.GET.get('print') else ['orders/order_details.html']


class CityListView(generic.ListView):
    model = City
    template_name = 'orders/city_list.html'
    paginate_by = 10


class ShopListView(generic.ListView):
    """
    Выводим список магазинов
    """
    template_name = 'orders/shop_list.html'
    paginate_by = 10

    def get_queryset(self):
        """
        отфильтруем город по параметру из query_string
        :return:
        """
        return Shop.objects.filter(city__slug=self.kwargs['city_slug'])

    #     return locals()
    #     если делать так, то контекст возвращается в objects_list

    def get_context_data(self, **kwargs):
        """
        добавим в контекст шаблона данные
        :param kwargs:
        :return:
        """
        context = super(ShopListView, self).get_context_data(**kwargs)
        context['city'] = get_object_or_404(City, slug=self.kwargs['city_slug'])
        return context


class CityCreateView(generic.CreateView):
    form_class = CityForm
    template_name = 'orders/add_city.html'

    # success_url = reverse('orders:city_list')
    # так не хочет работать, но работает с указанием ссылки - '/orders/city/'
    # приходится использовать get_success_url()

    def get_success_url(self):
        return reverse('orders:city_list')


class ShopFormView(generic.CreateView):
    form_class = ShopFormCBV
    template_name = 'orders/add_shopcbv.html'

    def get(self, request, *args, **kwargs):
        city = get_object_or_404(City, slug=self.kwargs['city_slug'])
        form = self.form_class(initial={'city': city})
        # context = self.get_context_data()
        # context.update(locals())
        return self.render_to_response(locals())
        # или так
        # return render(request, self.template_name, locals())
        # для пояснения хода мыслей
        # return render(request, self.template_name, {'form': form, 'city': city})
        # return render(request, self.template_name, {'form': form, 'city_slug': self.kwargs['city_slug']})

    def get_success_url(self):
        return reverse('orders:shop_list', kwargs=self.kwargs)
        # для наглядности
        # return reverse('orders:shop_list', kwargs={'city_slug': self.kwargs['city_slug']})

    def form_invalid(self, form):
        """
        отобразим форму, если не проходит проверку по unique_together
        :param form:
        :return:
        """
        city = get_object_or_404(City, slug=self.kwargs['city_slug'])
        return self.render_to_response(locals())
