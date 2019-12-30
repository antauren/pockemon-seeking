from django.db import models


class Pokemon(models.Model):
    img_url = models.ImageField(upload_to='images', verbose_name='Изображение')

    title_ru = models.CharField(max_length=200,
                                verbose_name='Название по-русски')

    title_en = models.CharField(max_length=200,
                                null=True,
                                blank=True,
                                verbose_name='Название по-английски',
                                default='')
    title_jp = models.CharField(max_length=200,
                                null=True,
                                blank=True,
                                verbose_name='Название по-японски',
                                default='')

    description = models.TextField(verbose_name='Описание',
                                   null=True,
                                   blank=True,
                                   default='')

    previous_evolution = models.ForeignKey('self',
                                           on_delete=models.SET_NULL,
                                           null=True,
                                           blank=True,
                                           verbose_name='Из кого эволюционировал')

    next_evolution = models.ForeignKey('self',
                                       on_delete=models.SET_NULL,
                                       null=True,
                                       blank=True,
                                       related_name='+',
                                       verbose_name='В кого эволюционирует')

    def __str__(self):
        return '{}'.format(self.title_ru)


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон')

    lat = models.FloatField(verbose_name='Координата широты')
    lon = models.FloatField(verbose_name='Координата долготы')

    level = models.IntegerField(null=True, blank=True, verbose_name='Уровень')
    health = models.IntegerField(null=True, blank=True, verbose_name='Здоровье')
    strength = models.IntegerField(null=True, blank=True, verbose_name='Атака')
    defence = models.IntegerField(null=True, blank=True, verbose_name='Защита')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='Выносливость')

    appeared_at = models.DateTimeField(null=True, blank=True, default=None, verbose_name='Дата появления')
    disappeared_at = models.DateTimeField(null=True, blank=True, default=None, verbose_name='Дата исчезновения')

    def __str__(self):
        return '{}'.format(self.pokemon)
