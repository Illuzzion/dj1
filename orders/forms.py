from django import forms

from .models import City, Shop, Order, OrderEntry


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = "__all__"

        # кроме поля slug
        exclude = ('slug',)

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Название города',
                'class': 'form-control'
            })
        }


class ShopFormCBV(forms.ModelForm):
    class Meta:
        model = Shop
        fields = "__all__"

        # это тоже часть Meta
        widgets = {
            'city': forms.HiddenInput(),
            'shop_name': forms.TextInput(attrs={
                'placeholder': 'Название магазина',
                'class': 'form-control'
            })
        }


class OrderEntryForm(forms.ModelForm):
    class Meta:
        model = OrderEntry
        fields = "__all__"

        widgets = {
            'order': forms.HiddenInput(),
            'shop': forms.Select(attrs={
                'class': 'form-control',
            }),
            'invoice_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер накладной'
            }),
            'place': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Количество мест'
            }),
        }


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
