from django.conf.urls import url

from . import views

app_name = 'orders'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^order/(?P<pk>[0-9]+)/detail/$', views.DetailView.as_view(), name='detail'),
]
