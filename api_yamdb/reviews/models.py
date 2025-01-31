from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import (MAX_COMMENT_LENGTH, MAX_NAME_LENGTH, MAX_SCORE,
                        MAX_SLUG_LENGTH, MAX_TEXT_LENGTH, MIN_SCORE)

User = get_user_model()


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField(
        max_length=MAX_NAME_LENGTH, verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True, max_length=MAX_SLUG_LENGTH, verbose_name='Слаг'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        """Возвращает текст категории."""
        return self.name


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField(
        max_length=MAX_NAME_LENGTH, verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True, max_length=MAX_SLUG_LENGTH, verbose_name='Слаг'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        """Возвращает текст жанра."""
        return self.name


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(
        max_length=MAX_NAME_LENGTH, verbose_name='Название'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель жанров и произведений (многие ко многим)."""

    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Связанные жанр - произведение'
        verbose_name_plural = 'Связанные жанры - произведения'

    def __str__(self):
        return f'{self.title} - {self.genre}'


class Review(models.Model):
    """Модель отзывов."""

    text = models.TextField(
        max_length=MAX_TEXT_LENGTH,
        verbose_name='Текст',
        help_text='Текст отзыва'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )

    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            MaxValueValidator(
                MAX_SCORE, message=f'Оценка не может быть больше {MAX_SCORE}'
            ),
            MinValueValidator(
                MIN_SCORE, message=f'Оценка не может быть меньше {MIN_SCORE}'
            ),
        ],
        help_text='Оценка произведения'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации отзыва',
    )

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
        ordering = ('pub_date',)

    def __str__(self):
        """Возвращает текст отзыва."""
        return self.text


class Comments(models.Model):
    """Модель комментариев."""

    text = models.TextField(
        max_length=MAX_COMMENT_LENGTH,
        verbose_name='Текст',
        help_text='Текст комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации комментария'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        """Возвращает текст комментария."""
        return self.text
