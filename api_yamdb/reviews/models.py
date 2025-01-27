from django.db import models

# Create your models here.
# Ресурсы API YaMDb


# Ресурс auth: аутентификация.

# Ресурс users: пользователи.

# Ресурс titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
class Title(models.Model):
    pass

# Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
# Одно произведение может быть привязано только к одной категории.


class Category(models.Model):
    pass

# Ресурс genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.


class Genre(models.Model):
    pass

# Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению.

# Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.
