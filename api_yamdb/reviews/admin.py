from django.contrib import admin

from .models import Category, Comments, Genre, Review, Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Title admin."""

    list_display = (
        'pk',
        'name',
        'year',
        'description',
    )
    list_filter = ('name', 'year')
    search_fields = ('name', 'year')
    empty_value_display = '-пусто-'

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'category', 'genre')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin."""

    list_display = (
        'pk',
        'name',
        'slug',
    )
    list_filter = ('name', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'

    class Meta:
        model = Category
        fileds = ('name', 'slug')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Genre admin."""

    list_display = (
        'pk',
        'name',
        'slug',
    )
    list_filter = ('name', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'

    class Meta:
        model = Genre
        fileds = ('name', 'slug')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Review admin."""

    list_display = (
        'pk',
        'title',
        'text',
        'author',
        'score',
        'pub_date',
    )
    list_filter = ('title', 'pub_date')
    search_fields = ('title', 'text')
    empty_value_display = '-пусто-'

    class Meta:
        model = Review
        fields = ('title', 'text', 'author', 'score', 'pub_date')


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    """Comments admin."""

    list_display = (
        'pk',
        'review',
        'text',
        'author',
        'pub_date',
    )
    list_filter = ('review', 'pub_date')
    search_fields = ('review', 'text')
    empty_value_display = '-пусто-'

    class Meta:
        model = Comments
        fields = ('review', 'text', 'author', 'pub_date')
