from django import forms
from .models import City, Shop, Order, OrderEntry


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        # выведем все поля
        fields = "__all__"

        # кроме поля slug
        exclude = ('slug',)

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Название города',
                'class': 'form-control'
            })
        }

        labels = {
            'name': 'Город',
        }


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = "__all__"
        exclude = ('city',)

        widgets = {
            'shop_name': forms.TextInput(attrs={
                'placeholder': 'Название магазина',
                'class': 'form-control'
            })
        }


class ShopFormCBV(forms.ModelForm):
    class Meta:
        model = Shop
        fields = "__all__"

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
        # exclude = ('order',)

        # widgets = {
            # 'shop': forms.ModelChoiceField(OrderEntry.shop.objects.all(), atttrs={
            #     'class': 'form-control',
            # }),
            # 'place': forms.IntegerField(attrs={
            #     'class': 'form-control'
            # })
        # }
