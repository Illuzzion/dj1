"""dj1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from orders import views

from registration.backends.default.views import RegistrationView
from django.core.urlresolvers import reverse


class MyRegistrationView(RegistrationView):
    def get_success_url(self, user=None):
        return 'rango/add_profile/'
        # return reverse('rango:add_profile')


urlpatterns = [
    url(r'^$', views.OrderIndexView.as_view(), name='index'),
    url(r'^polls/', include('polls.urls')),
    url(r'^orders/', include('orders.urls')),
    url(r'^rango/', include('rango.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^testapp/', include('testapp.urls')),

    # Добавляем эту строку в URL шаблоны, чтобы переопределить шаблон, используемый по умолчанию для учетных записей, - r'^accounts/'.
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),

    # url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
]
