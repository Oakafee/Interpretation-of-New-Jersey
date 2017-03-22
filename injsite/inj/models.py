from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils.text import slugify

class Article(models.Model):
	title = models.CharField(max_length=200, editable=False, unique=True)
	subtitle = models.CharField(max_length=200)
	author = models.CharField(max_length=200, default="Jesse Fried")
	article_content = models.CharField(max_length=50000)
	pub_date = models.DateTimeField('date published', auto_now=True, editable=False,)
	parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)	
	slug = models.SlugField(max_length=50, default="",)
	main_cat = models.BooleanField(default=False)
	html_safe = models.BooleanField(default=False)
	comments = models.BooleanField(default=True)
	def __str__(self):
		return self.title
	def save(self, *args, **kwargs):
	    if not self.slug:
	    	self.slug = slugify(self.title,)
	    super(Article, self).save(*args, **kwargs)

class Commentary(models.Model):
	article = models.ForeignKey(Article, on_delete=models.CASCADE)
	com_title = models.CharField(max_length=200)
	com_author = models.CharField(max_length=200)
	commentary = models.CharField(max_length=50000)
	pub_date = models.DateTimeField('date published', auto_now=True, editable=False,)
	def __str__(self):
		return self.com_title