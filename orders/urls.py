from django.conf.urls import url

from . import views

app_name = 'orders'

urlpatterns = [
    url(r'^$', views.OrderIndexView.as_view(), name='index'),

    url(r'^city/$', views.CityListView.as_view(), name='city_list'),
    # url(r'^city/add/$', views.add_city, name='add_city'),
    url(r'^city/add/$', views.CityCreateView.as_view(), name='add_city'),

    url(r'^city/(?P<city_slug>[\w\-]+)/$', views.ShopListView.as_view(), name='shop_list'),
    # fbv
    # url(r'^city/(?P<city_slug>[\w\-]+)/add-shop/$', views.add_shop, name='add_shop'),

    # cbv
    url(r'^city/(?P<city_slug>[\w\-]+)/add-shopcbv/$', views.ShopFormView.as_view(), name='add_shopcbv'),

    url(r'^order/new/$', views.OrderCreateView.as_view(), name='new_order'),
    url(r'^order/(?P<pk>[0-9]+)/detail/$', views.OrderDetailView.as_view(), name='order_details'),
]
