import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


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
    name = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "content\".\"genre_film_work"


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField(_('Full Name'), null=False)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        return self.full_name


class PersonFilmWork(UUIDMixin):
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    role = models.TextField(_('Role'), null=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"


class FilmTypes(models.TextChoices):
    MOVIE = 'movie', _('Movie')
    TVSHOW = 'tv_show', _('Show')


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('Title'), max_length=255, null=False)
    description = models.TextField(_('Description'), blank=True)
    creation_date = models.DateField(blank=True, verbose_name=_('Date'))
    rating = models.FloatField(
        _('Rate'),
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
        )
    type = models.CharField(
        max_length=10,
        choices=FilmTypes.choices,
        verbose_name=_('Type')
    )
    certificate = models.CharField(
        _('Certificate'),
        max_length=512,
        blank=True
        )
    file_path = models.FileField(
        _('File'), blank=True,
        null=True,
        upload_to='movies/'
        )
    genres = models.ManyToManyField(
        Genre,
        through='GenreFilmwork',
        verbose_name=_('Genre')
        )
    persons = models.ManyToManyField(
        Person,
        through='PersonFilmWork',
        verbose_name=_('Genre')
        )

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Movie')
        verbose_name_plural = _('Movies')

    def __str__(self):
        return self.title
