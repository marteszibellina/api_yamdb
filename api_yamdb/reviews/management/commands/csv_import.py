"""Модуль для импорта csv-файлов в базу данных."""

import csv
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Comments, Genre, Review, Title

User = get_user_model()


class Command(BaseCommand):
    """Команда для импорта csv-файлов в базу данных."""
    help = 'Импорт сsv-файлов в базу данных'

    def handle_users(self, *args, **kwargs):
        """Функция для импорта csv-файлов users в базу данных."""
        with open(
            Path(settings.BASE_DIR) / 'static/data/users.csv', 'r',
            encoding='utf-8'
        ) as csv_file:
            for row in csv.DictReader(csv_file):
                User.objects.create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )

    def handle_category(self, *args, **kwargs):
        """Функция для импорта csv-файлов category в базу данных."""
        with open(
            Path(settings.BASE_DIR) / 'static/data/category.csv', 'r',
            encoding='utf-8'
        ) as csv_file:
            for row in csv.DictReader(csv_file):
                Category.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )

    def handle_comments(self, *args, **kwargs):
        """Функция для импорта csv-файлов comments в базу данных."""
        with open(
            Path(settings.BASE_DIR) / 'static/data/comments.csv', 'r',
            encoding='utf-8'
        ) as csv_file:
            for row in csv.DictReader(csv_file):
                # Проверка наличия связанных записей в User и Review
                if User.objects.filter(
                    id=row['author']).exists() and Review.objects.filter(
                        id=row['review_id']).exists():
                    Comments.objects.create(
                        id=row['id'],
                        review_id=row['review_id'],
                        text=row['text'],
                        author_id=row['author'],
                        pub_date=row['pub_date'],
                    )
                else:
                    print(
                        f'Skipping comment {row["id"]}',
                        ' - related User or Review does not exist.',
                    )

    def handle_genre_title(self, *args, **kwargs):
        """Функция для импорта csv-файлов genre_title в базу данных."""
        with open(
            Path(settings.BASE_DIR) / 'static/data/genre_title.csv', 'r',
            encoding='utf-8'
        ) as csv_file:
            for row in csv.DictReader(csv_file):
                try:
                    title = Title.objects.get(id=row['title_id'])
                    genre = Genre.objects.get(id=row['genre_id'])

                    # Добавляем Genre к Title
                    title.genres.add(genre)

                except Title.DoesNotExist:
                    print(f"Title with id {row['title_id']} does not exist.")
                except Genre.DoesNotExist:
                    print(f"Genre with id {row['genre_id']} does not exist.")

    def handle_genre(self, *args, **kwargs):
        """Функция для импорта csv-файлов genre в базу данных."""
        with open(
            Path(settings.BASE_DIR) / 'static/data/genre.csv', 'r',
            encoding='utf-8'
        ) as csv_file:
            for row in csv.DictReader(csv_file):
                Genre.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )

    def handle_review(self, *args, **kwargs):
        """Функция для импорта csv-файлов review в базу данных."""
        with open(
            Path(settings.BASE_DIR) / 'static/data/review.csv', 'r',
            encoding='utf-8'
        ) as csv_file:
            for row in csv.DictReader(csv_file):
                try:
                    # Проверяем, существует ли пользователь и заголовок
                    author = User.objects.get(id=row['author'])
                    title = Title.objects.get(id=row['title_id'])

                    # Создаем отзыв
                    Review.objects.create(
                        id=row['id'],
                        text=row['text'],
                        score=row['score'],
                        pub_date=row['pub_date'],
                        author=author,
                        title=title,
                    )

                except User.DoesNotExist:
                    print(f'User with id {row["author"]} does not exist.')
                except Title.DoesNotExist:
                    print(f'Title with id {row["title_id"]} does not exist.')

    def handle_titles(self, *args, **kwargs):
        """Функция для импорта csv-файлов titles в базу данных."""
        with open(
            Path(settings.BASE_DIR) / 'static/data/titles.csv', 'r',
            encoding='utf-8'
        ) as csv_file:
            for row in csv.DictReader(csv_file):
                Title.objects.create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category'],
                )

    def handle(self, *args, **kwargs):
        self.handle_users()
        self.handle_category()
        self.handle_comments()
        self.handle_genre_title()
        self.handle_genre()
        self.handle_review()
        self.handle_titles()
