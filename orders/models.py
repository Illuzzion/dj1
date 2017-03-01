from django.db import models
from uuslug import slugify


class City(models.Model):
    """
    Города
    """
    name = models.CharField(max_length=100, verbose_name="Название города", unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = "Города"
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # создадим слаг города по имени
        self.slug = slugify(self.name)

        super(City, self).save(*args, **kwargs)


class Shop(models.Model):
    """
    Магазины в городах
    """
    city = models.ForeignKey(City, verbose_name="Название города")
    shop_name = models.CharField(max_length=200, verbose_name="Название магазина")

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Магазины"
        unique_together = ('city', 'shop_name')
        ordering = ('city', 'shop_name')

    def __str__(self):
        return "{}, {}".format(self.city.name, self.shop_name)

    def save(self, *args, **kwargs):
        try:
            super(Shop, self).save(*args, **kwargs)
        except Exception as e:
            print('error', e)


class Order(models.Model):
    """
    Заказы
    """
    date = models.DateTimeField(verbose_name="Создано", auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return str(self.id)


class OrderEntry(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ')
    shop = models.ForeignKey(Shop, verbose_name='Магазин')
    invoice_number = models.PositiveSmallIntegerField(verbose_name='Номер накладной')
    place = models.PositiveSmallIntegerField(verbose_name='Количество мест', default=1)

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
        unique_together = ('order', 'invoice_number')

    def __str__(self):
        return "Упаковочный лист №{}, {}, номер накладной {}".format(self.order, self.shop, self.invoice_number)
