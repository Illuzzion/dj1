from django.conf.urls import url

from . import views

app_name = 'orders'

urlpatterns = [
    # главная страница
    url(r'^$', views.OrderIndexView.as_view(), name='index'),

    # список всех городов
    url(r'^city/$', views.CityListView.as_view(), name='city_list'),

    # добавление города
    url(r'^city/add/$', views.CityCreateView.as_view(), name='add_city'),

    # список магазинов выбранного города
    url(r'^city/(?P<city_slug>[\w\-]+)/$', views.ShopListView.as_view(), name='shop_list'),

    # все магазины
    url(r'^shops/$', views.ShopListView.as_view(), name='all_shops_list'),

    # добавить магазин в выбранный город
    url(r'^city/(?P<city_slug>[\w\-]+)/add-shop/$', views.ShopFormView.as_view(), name='add_shopcbv'),

    # удалить город
    url(r'^city/(?P<slug>[\w\-]+)/delete/$', views.CityDeleteView.as_view(), name='delete_city'),

    # удалить магазин
    url(r'^city/(?P<slug>[\w\-]+)/shop/(?P<pk>[\d]+)/delete/$', views.ShopDeleteView.as_view(), name='delete_shop'),

    # новый упаковочный лист
    url(r'^order/new/$', views.OrderCreateView.as_view(), name='new_order'),

    # просмотр упаковочного листа
    url(r'^order/(?P<pk>[0-9]+)/detail/$', views.OrderDetailView.as_view(), name='order_details'),
]
