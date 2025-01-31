import csv

from django.core.management.base import BaseCommand

from reviews.models import (
    Category,
    Genre,
    GenreTitle,
    Review,
    Title,
    Comments
)
from users.models import User


class Command(BaseCommand):
    help = 'Импорт сsv-файлов в базу данных'

    def handle(self, *args, **kwargs):
        users = kwargs['users']
        category = kwargs['category']
        comments = kwargs['comments']
        genre_title = kwargs['genre_title']
        genre = kwargs['genre']
        review = kwargs['review']
        titles = kwargs['titles']

        if users:
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
        if category:
            with open(
                'static/data/category.csv', 'r', encoding='utf-8'
            ) as csv_file:
                for row in csv.DictReader(csv_file):
                    Category.objects.create(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug'],
                    )
        if comments:
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
        if genre_title:
            with open(
                'static/data/genre_title.csv', 'r', encoding='utf-8'
            ) as csv_file:
                for row in csv.DictReader(csv_file):
                    GenreTitle.objects.create(
                        id=row['id'],
                        genre_id=row['genre_id'],
                        title_id=row['title_id'],
                    )
        if genre:
            with open(
                'static/data/genre.csv', 'r', encoding='utf-8'
            ) as csv_file:
                for row in csv.DictReader(csv_file):
                    Genre.objects.create(
                        id=row['id'],
                        name=row['name'],
                        slug=row['slug'],
                    )
        if review:
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
        if titles:
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

    def add_arguments(self, parser):
        parser.add_argument(
            '-u',
            '--users',
            action='store_true',
            default=False,
            help='Импорт из файла "users.csv"'
        )
        parser.add_argument(
            '-ct',
            '--category',
            action='store_true',
            default=False,
            help='Импорт из файла "category.csv"'
        )
        parser.add_argument(
            '-cm',
            '--comments',
            action='store_true',
            default=False,
            help='Импорт из файла "comments.csv"'
        )
        parser.add_argument(
            '-gt',
            '--genre_title',
            action='store_true',
            default=False,
            help='Импорт из файла "genre_title.csv"'
        )
        parser.add_argument(
            '-g',
            '--genre',
            action='store_true',
            default=False,
            help='Импорт из файла "genre.csv"'
        )
        parser.add_argument(
            '-r',
            '--review',
            action='store_true',
            default=False,
            help='Импорт из файла "review.csv"'
        )
        parser.add_argument(
            '-t',
            '--titles',
            action='store_true',
            default=False,
            help='Импорт из файла "titles.csv"'
        )
