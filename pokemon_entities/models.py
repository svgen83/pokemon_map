from django.db import models


class Pokemon(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200,
                             verbose_name='русское название')
    title_en = models.CharField(max_length=200,
                                verbose_name='английское название',
                                null=True, blank=True)
    title_jap = models.CharField(max_length=200,
                                 verbose_name='японское название',
                                 null=True, blank=True)
    image = models.ImageField(upload_to='images',
                              verbose_name='изображение')
    description = models.TextField(max_length=2000,
                                   verbose_name='описание',
                                   blank=True, default='')
    previous_evolution = models.ForeignKey(
        'self', null=True, blank=True,
        verbose_name='в кого эволюционирует',
        related_name='next_evolutions',
        on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, verbose_name='покемон',
                                on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True,
                                 verbose_name='широта')
    longitude = models.FloatField(null=True, blank=True,
                                  verbose_name='долгота')
    appeared_at = models.DateTimeField(null=True, blank=True,
                                       verbose_name='время появления')
    disappeared_at = models.DateTimeField(null=True, blank=True,
                                          verbose_name='время исчезновения')
    level = models.IntegerField(default=0, verbose_name='уровень')
    health = models.IntegerField(default=0, verbose_name='здоровье')
    strength = models.IntegerField(default=0, verbose_name='сила')
    defence = models.IntegerField(default=0, verbose_name='сопротивление')
    stamina = models.IntegerField(default=0, verbose_name='выносливость')
