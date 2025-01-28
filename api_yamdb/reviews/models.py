from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import (MAX_TEXT_LENGTH,
                        MAX_COMMENT_LENGTH,
                        MAX_SCORE, MIN_SCORE)

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
    # Временная модель автора, пока не реализована модель пользователей
    author = models.IntegerField('ID автора')

    # author = models.ForeignKey(
    #     'users.User',
    #     on_delete=models.CASCADE,
    #     verbose_name='Автор'
    # )

    score = models.PositiveSmallIntegerField(
        "Оценка",
        validators=[
            MaxValueValidator(
                MAX_SCORE, message=f"Оценка не может быть больше {MAX_SCORE}"
            ),
            MinValueValidator(
                MIN_SCORE, message=f"Оценка не может быть меньше {MIN_SCORE}"
            ),
        ],
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        """Возвращает текст отзыва."""
        return self.text


class Comments(models.Model):
    """Модель комментариев."""

    text = models.TextField('Текст', max_length=MAX_COMMENT_LENGTH)
    review = models.ForeignKey(
        'reviews.Reviews',
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    # Временная модель автора, пока не реализована модель пользователей
    author = models.IntegerField('ID автора комментария')

    # author = models.ForeignKey(
    #     'users.User',
    #     on_delete=models.CASCADE,
    #     verbose_name='Автор комментария'
    # )

    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        """Возвращает текст комментария."""
        return self.text
