import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genre')

    def __str__(self):
        return self.name

class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=255)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        return self.full_name

class Filmwork(UUIDMixin, TimeStampedMixin):
    class TypeChoices(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'tv_show', _('tv_show')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation_date'))
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    type = models.CharField(_('type'), choices=TypeChoices.choices, max_length=255)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Movie')
        verbose_name_plural = _('Movies')

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(Filmwork, verbose_name=_('movie'), on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, verbose_name=_('genre'), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('GenreFilmwork')
        verbose_name_plural = _('GenresFilmworks')
        indexes = [models.Index(fields=['film_work', 'genre'], name='film_work_genre_idx')]
        constraints = [models.UniqueConstraint(fields=['film_work', 'genre'], name='unique film_work_genre')]

    def __str__(self):
        return self.film_work.title

class PersonFilmwork(UUIDMixin):
    class RoleChoices(models.TextChoices):
        ACTOR = 'actor', _('actor')
        WRITER = 'writer', _('writer')
        DIRECTOR = 'director', _('director')

    film_work = models.ForeignKey(Filmwork, verbose_name=_('movie'), on_delete=models.CASCADE)
    person = models.ForeignKey(Person, verbose_name=_('person'), on_delete=models.CASCADE)
    role = models.CharField(_('role'), choices=RoleChoices.choices, max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('PersonFilmwork')
        verbose_name_plural = _('PersonsFilmworks')
        indexes = [models.Index(fields=['film_work', 'person'], name='film_work_person_idx')]
        constraints = [models.UniqueConstraint(fields=['film_work', 'person'], name='unique film_work_person')]

    def __str__(self):
        return self.film_work.title
