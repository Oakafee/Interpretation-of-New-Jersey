from __future__ import unicode_literals

from django.db import models

class Test(models.Model):
	text_text = models.CharField(max_length=200)
	def __str__(self):
		return self.com_title
