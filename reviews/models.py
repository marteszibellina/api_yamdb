"""Модели отзывов и комментариев."""

from django.db import models

from .consts import MAX_COMMENT_LENGTH, MAX_TEXT_LENGTH


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

    def __str__(self):
        return self.text


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

    def __str__(self):
        return self.text
