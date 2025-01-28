"""reviews admin."""

from django.contrib import admin
from .models import Reviews, Comments


admin.site.register(Reviews)
admin.site.register(Comments)
