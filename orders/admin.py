from django.contrib import admin

from .models import City, Shop, Order, OrderEntry


class CityAdmin(admin.ModelAdmin):
    # можем указать список отображаемых полей
    # list_display = ('name', 'slug')

    # получаем список всех доступных полей через мета модели
    list_display = [f.name for f in City._meta.fields]

    # фильтр для указаных полей
    list_filter = ('name',)

    # поиск по указанным полям (регистрозависим)
    search_fields = ('name',)

    # все поля кроме этих
    # exclude = ('slug',)

    # class Meta:
    #     model = City


admin.site.register(City, CityAdmin)


class ShopAdmin(admin.ModelAdmin):
    list_display = ('city', 'shop_name')


admin.site.register(Shop, ShopAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date',)

    class Meta:
        model = Order


admin.site.register(Order, OrderAdmin)

# class OrderEntryAdmin(admin.ModelAdmin):
#     list_display = ('order', 'shop', 'place')


admin.site.register(OrderEntry)
