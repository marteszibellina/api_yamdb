from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import (MAX_TEXT_LENGTH,
                        MAX_COMMENT_LENGTH,
                        MAX_SCORE, MIN_SCORE)


# Ресурс auth: аутентификация.

# Ресурс users: пользователи.


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        """Возвращает текст категории."""
        return self.slug


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        """Возвращает текст жанра."""
        return self.slug


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True
    )


class GenreTitle(models.Model):
    """Модель жанров и произведений (многие ко многим)."""

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
        constraints = [
            # Проверка уникальности отзыва на уровне БД
            # на случай, если будут параллельные запросы или ошибке в логике
            # самого приложения
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]
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
