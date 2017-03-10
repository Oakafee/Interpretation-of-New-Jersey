from django.conf.urls import url

from . import views

app_name = 'inj'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^story/$', views.story, name='story'),
	url(r'^newarticle/$', views.newarticle, name='newarticle'),
	url(r'^addarticle/$', views.addarticle, name='addarticle'),
	url(r'^(?P<slug>[\w-]+)/$', views.article, name='article'),
	url(r'^(?P<slug>[\w-]+)/addcomment/$', views.addcomment, name='addcomment'),
	url(r'^(?P<slug>[\w-]+)/edit/$', views.edit, name='edit'),
	url(r'^(?P<slug>[\w-]+)/changearticle/$', views.changearticle, name='changearticle'),
]