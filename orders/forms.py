from django import forms
from .models import City, Shop, Order


class CityForm(forms.ModelForm):
    name = forms.CharField(max_length=100, help_text='Введите название города')
    slug = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = City
        exclude = ('slug',)


class ShopForm(forms.ModelForm):
    name = forms.CharField(max_length=200, help_text='Введите название магазина')
    city = forms.CharField(widget=forms.HiddenInput, initial=0, required=False)

    class Meta:
        model = Shop
        exclude = ('city',)

#
#
# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
