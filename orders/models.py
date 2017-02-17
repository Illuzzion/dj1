from django.db import models
from django.utils.text import slugify


class City(models.Model):
    """
    Города
    """
    name = models.CharField(max_length=100, verbose_name="Название города")
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = "Города"
        ordering = ('name',)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(City, self).save(*args, **kwargs)


# Choices are: city, city_id, id, order, shop_name
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
        # unique_together = (('city', 'shop_name'),)
        ordering = ('city', 'shop_name')


class Order(models.Model):
    """
    Заказы
    """
    entry = models.ManyToManyField(Shop)
    date = models.DateTimeField(verbose_name="Создано", auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

#
# class Artist(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#
#     @property
#     def albums(self):
#         songs = self.song_set.all()
#         return Album.objects.filter(song_set__in=songs)
#
#
# class Album(models.Model):
#     name = models.CharField(max_length=50)
#     # release_date = models.DateField()
#
#     @property
#     def artists(self):
#         songs = self.song_set.all()
#         return Artist.objects.filter(song_set__in=songs)
#
#
# class Song(models.Model):
#     artists = models.ManyToManyField(Artist)
#     albums = models.ManyToManyField(Album)
#     name = models.CharField(max_length=100)
#     # release_date = models.DateField()
