from django.db import models

# Create your models here.
# Ресурсы API YaMDb


# Ресурс auth: аутентификация.

# Ресурс users: пользователи.

# Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
# Одно произведение может быть привязано только к одной категории.


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.slug

# Ресурс genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.slug
# Ресурс titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True
    )


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE,
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE
    )

# Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению.

# Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.
