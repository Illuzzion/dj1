from django.contrib import admin

from .models import City, Shop, Order, OrderEntry
from .forms import CityAdminForm


class CityAdmin(admin.ModelAdmin):
    # можем указать список отображаемых полей
    # list_display = ('name', 'slug')
    form = CityAdminForm

    # получаем список всех доступных полей через мета модели
    # list_display = [f.name for f in City._meta.fields]
    # list_display = ('id', 'name')
    exclude = ('slug',)

    # фильтр для указаных полей
    list_filter = ('name',)

    # поиск по указанным полям (регистрозависим)
    search_fields = ('name', 'slug')

    # пагинация
    list_per_page = 18

    # сортировка
    ordering = ['-id']
    # actions_on_bottom = True

    # автоматически заполнять поле 'slug' по полю 'name'
    # prepopulated_fields = {'slug': ('name',)}

    # все поля кроме этих
    # exclude = ('slug',)

    # class Meta:
    #     model = City


admin.site.register(City, CityAdmin)


class ShopAdmin(admin.ModelAdmin):
    list_display = ('city', 'shop_name')
    list_filter = ('city',)
    ordering = ['-id']
    list_per_page = 20


admin.site.register(Shop, ShopAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date',)

    class Meta:
        model = Order


admin.site.register(Order, OrderAdmin)


class OrderEntryAdmin(admin.ModelAdmin):
    list_display = ('order', 'shop')
    ordering = ["-id"]
    list_filter = ('order',)


admin.site.register(OrderEntry, OrderEntryAdmin)
