from django.db import models

from .constants import MAX_TEXT_LENGTH, MAX_COMMENT_LENGTH

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


class Reviews(models.Model):
    """Модель отзывов."""

    text = models.TextField('Текст', max_length=MAX_TEXT_LENGTH)
    title = models.ForeignKey(
        'titles.Title',
        on_delete=models.CASCADE,
        verbose_name='Название'
    )
    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField('Оценка')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comments(models.Model):
    """Модель комментариев."""

    text = models.TextField('Текст', max_length=MAX_COMMENT_LENGTH)
    review = models.ForeignKey(
        'reviews.Reviews',
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
