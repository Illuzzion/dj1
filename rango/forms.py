from django import forms
from .models import Category, Page


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text='Please enter the category name')
    views = forms.IntegerField(widget=forms.HiddenInput, initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        # Добавим связь между ModelForm и моделью
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    """
    Класс формы для модели страницы(Page)
    """
    title = forms.CharField(max_length=128, help_text="Please enter title of the page")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page")
    views = forms.IntegerField(widget=forms.HiddenInput, initial=0)

    class Meta:
        model = Page
        # Какие поля мы хотим добавить в форму?
        # Сейчас нам не нужны все поля из модели
        # Некоторые поля могут принимать значение NULL, мы не будем их добавлять
        # Спрячем внешний ключ, мы можем исключить поле category из формы так
        exclude = ('category',)
        # или укажем конкретные поля для вывода (исключая поле category)
        # fields = ('title', 'url', 'views')

    def clean(self):
        """
        Перегрузим родительскую функцию clean()
        :return: dict
        """
        # у родителя этого класса (т.е. forms.ModelForm), есть словарь с очищенными данными - cleaned_data
        cleaned_data = self.cleaned_data
        # получаем из него url
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data

