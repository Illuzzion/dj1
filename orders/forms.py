from django import forms
from .models import City, Shop, Order


class CityForm(forms.ModelForm):
    name = forms.CharField(max_length=100, help_text='Please enter the City name')

    class Meta:
        model = City


class ShopForm(forms.ModelForm):
    name = forms.CharField(max_length=200, help_text='Please enter the Shop name')

    class Meta:
        model = Shop
        exclude = ('city',)
