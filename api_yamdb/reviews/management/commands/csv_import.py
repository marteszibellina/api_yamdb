"""Модуль для импорта csv-файлов в базу данных."""

# import csv
from csv import DictReader
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Comments, Genre, Review, Title

User = get_user_model()


class Command(BaseCommand):
    """
    Команда для импорта данных из csv-файлов в базу данных:
    управление на python.py csv_import

    Если вам нужно обновить базу данных:
    1) Удалите db.sqlite3
    2) Выполните миграцию (python manage.py migrate --run-syncdb).

    Появится новая пустая база данных.
    """
    help = "Loading data from csv files."

    def handle(self, *args, **options):

        for row in DictReader(
                open(Path(settings.BASE_DIR) / 'static/data/category.csv',
                     encoding='utf-8')):
            category = Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            category.save()

        for row in DictReader(
                open(Path(settings.BASE_DIR) / 'static/data/genre.csv',
                     encoding='utf-8')):
            genre = Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            genre.save()

        for row in DictReader(
                open(Path(settings.BASE_DIR) / 'static/data/titles.csv',
                     encoding='utf-8')):
            title = Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category_id=row['category'],
            )
            title.save()

        for row in DictReader(
                open(Path(settings.BASE_DIR) / 'static/data/users.csv',
                     encoding='utf-8')):
            user = User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name'],
            )
            user.save()

        for row in DictReader(
                open(Path(settings.BASE_DIR) / 'static/data/review.csv',
                     encoding='utf-8')):
            review = Review(
                id=row['id'],
                title_id=row['title_id'],
                text=row['text'],
                author_id=row['author'],
                score=row['score'],
                pub_date=row['pub_date'],
            )
            review.save()

        for row in DictReader(
                open(Path(settings.BASE_DIR) / 'static/data/comments.csv',
                     encoding='utf-8')):
            comments = Comments(
                id=row['id'],
                review_id=row['review_id'],
                text=row['text'],
                author_id=row['author'],
                pub_date=row['pub_date'],
            )
            comments.save()

        for row in DictReader(
                open(Path(settings.BASE_DIR) / 'static/data/genre_title.csv',
                     encoding='utf-8')
        ):
            genre = Genre.objects.get(id=row['genre_id'])
            title = Title.objects.get(id=row['title_id'])
            title.genre.add(genre)
