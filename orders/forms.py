from django import forms
from .models import City, Shop, Order


class CityForm(forms.ModelForm):
    # name = forms.CharField(max_length=100, help_text='Введите название города')
    # slug = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = City
        # выведем все поля
        fields = "__all__"

        # кроме поля slug
        exclude = ('slug',)

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Название города',
                'class': 'formcontrol'
            })
        }

        labels = {
            'name': 'Город',
        }


class ShopForm(forms.ModelForm):
    # name = forms.CharField(max_length=200, help_text='Введите название магазина')
    # city = forms.CharField(widget=forms.HiddenInput, initial=0, required=False)

    class Meta:
        model = Shop
        fields = "__all__"
        # exclude = ('city',)
