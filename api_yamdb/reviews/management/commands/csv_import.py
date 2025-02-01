import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Comments, Genre, Review, Title
from users.models import User


class Command(BaseCommand):
    help = 'Импорт сsv-файлов в базу данных'

    def handle_users(self, *args, **kwargs):
        with open(
                'static/data/users.csv', 'r', encoding='utf-8'
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
        with open(
                'static/data/category.csv', 'r', encoding='utf-8'
        ) as csv_file:
            for row in csv.DictReader(csv_file):
                Category.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )

    def handle_comments(self, *args, **kwargs):
        with open(
            'static/data/comments.csv', 'r', encoding='utf-8'
        ) as csv_file:
            for row in csv.DictReader(csv_file):
                Comments.objects.create(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author_id=row['author'],
                    pub_date=row['pub_date'],
                )

    def handle_genre_title(self, *args, **kwargs):
        with open(
            'static/data/genre_title.csv', 'r', encoding='utf-8'
        ) as csv_file:
            for row in csv.DictReader(csv_file):
                Title.objects.create(
                    id=row['id'],
                    genre_id=row['genre_id'],
                    title_id=row['title_id'],
                )

    def handle_genre(self, *args, **kwargs):
        with open(
            'static/data/genre.csv', 'r', encoding='utf-8'
        ) as csv_file:
            for row in csv.DictReader(csv_file):
                Genre.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )

    def handle_review(self, *args, **kwargs):
        with open(
            'static/data/review.csv', 'r', encoding='utf-8'
        ) as csv_file:
            for row in csv.DictReader(csv_file):
                Review.objects.create(
                    id=row['id'],
                    text=row['text'],
                    score=row['score'],
                    pub_date=row['pub_date'],
                    author_id=row['author'],
                    title_id=row['title_id'],
                )

    def handle_titles(self, *args, **kwargs):
        with open(
            'static/data/titles.csv', 'r', encoding='utf-8'
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
