from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmWork, Person, PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',)


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmWork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmWork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,)
    list_display = ('title', 'type', 'creation_date', 'rating',)
    list_filter = ('type', 'genres')
    search_fields = ('title', 'description', 'id')
