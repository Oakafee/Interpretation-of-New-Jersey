from django.contrib import admin

# Register your models here.
from .models import Article, Commentary

admin.site.register(Article)
admin.site.register(Commentary)