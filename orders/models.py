from django.db import models
from uuslug import slugify


class City(models.Model):
    """
    Города
    """
    name = models.CharField(max_length=100, verbose_name="Название города", unique=True)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = "Города"
        ordering = ('name',)

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

    def __str__(self):
        return "г.{}, {}".format(self.city.name, self.shop_name)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Магазины"
        unique_together = ('city', 'shop_name')
        ordering = ('city', 'shop_name')


class Order(models.Model):
    """
    Заказы
    """
    # entry = models.ManyToManyField(Shop, through='OrderEntry')
    date = models.DateTimeField(verbose_name="Создано", auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderEntry(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ')
    shop = models.ForeignKey(Shop, verbose_name='Магазин')
    place = models.IntegerField(verbose_name='Место')

    def __str__(self):
        return "Заказ №{}, {}, место {}".format(self.order, self.shop, self.place)

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'