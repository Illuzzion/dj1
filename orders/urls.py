from django.conf.urls import url

from . import views

app_name = 'orders'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^city/$', views.CityListView.as_view(), name='city_list'),
    url(r'^city/add$', views.add_city, name='add_city'),

    url(r'^city/(?P<city_slug>[\w\-]+)/$', views.ShopListView.as_view(), name='shop_list'),
    url(r'^city/(?P<city_slug>[\w\-]+)/add-shop/$', views.add_shop, name='add_shop'),

    url(r'^order/(?P<pk>[0-9]+)/detail/$', views.OrderDetailView.as_view(), name='detail'),
    # url(r'^order/add/$')
]
