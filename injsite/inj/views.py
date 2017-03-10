from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse
from django.views import generic
from django.db import IntegrityError

from django.utils.text import slugify

from .models import Article

def index(request):
	return HttpResponseRedirect(reverse('inj:article', args=('welcome',)))

def getchart():
	chart = getmaincats()
	context = {
		'chart': chart,
	}
	return context

def story(request):
	html = getmaincats()
	return HttpResponse(html)

def getmaincats():
	html = '<ul class="chart">'
	article_list = Article.objects.order_by('slug')
	for i in range(len(article_list)*5):
		try:
			article = article_list.get(pk=i)
			if article.main_cat:
				html += list_and_link(article.title, expand=False) + getchildren(article.title, show=True)
		except Article.DoesNotExist:
			cat = 0		
	html += "</ul>"
	return html

def getchildren(title, show):
	html = is_visible(title, show)
	article = Article.objects.get(title=title)
	try:
		children = article.article_set.order_by('slug')
		if children:
			for child in children:
				html += list_and_link(child.title, expand=True) + getchildren(child.title, show=False)
	except Article.DoesNotExist: pass
	html += "</ul>"
	return html

def list_and_link(title, expand):
	article = Article.objects.get(title=title)
	if expand:
		if article.article_set.all(): expand = True
		else: expand = False
	list_link = '<li>'
	if expand:
		list_link += '<div class="expand">+</div>&nbsp;'
	else:
		list_link += '<div class="expand-placeholder">+</div>&nbsp;'	
	list_link += '<a href="../' + article.slug + '">' + article.title + '</a></li>'
	return list_link
	
def is_visible(title, show):
	html = '<ul class="chart'
	article = Article.objects.get(title=title)
	if show == False: html += ' hidden'
	html += '">'	
	return html
	
def article(request, slug):
	article = get_object_or_404(Article, slug=slug)
	context = getchart()
	context['article'] = article
	return render(request, 'inj/article.html', context)

def addcomment(request, slug):
	article = get_object_or_404(Article, slug=slug)
	com = article.commentary_set
	com_title = request.POST['title']
	com_author = request.POST['author']
	commentary = request.POST['comment']
	if commentary != "" and commentary != "Please type or paste your text here.":
		com.create(com_title=com_title, com_author=com_author, commentary=commentary)
		return HttpResponseRedirect(reverse('inj:article', args=(article.slug,)))
	else:
		return render(request, 'inj/article.html', {
		'article': article,
		'error_message': "That wasn't a valid comment. Please try again.",
		})

def newarticle(request):
	return render(request, 'inj/newarticle.html')

def addarticle(request):
	try:
		title = request.POST['title']
		Article.objects.create(title=title)
	except (KeyError):
		return HttpResponse("Didn't work")
	except (IntegrityError):
		return HttpResponse("We already have an article with that title. Please find that one and add your comments to it, or make an article with a different title.")
	else:
		new_article = Article.objects.get(title=title)
		new_article.subtitle = request.POST['subtitle']
		new_article.author = request.POST['author']
		new_article.article_content = request.POST['content']	
		new_article.html_safe = request.POST['html-safe']
		parent = Article.objects.get(title=request.POST['parent'])	
		new_article.parent = parent
		new_article.save()		
		return HttpResponseRedirect(reverse('inj:article', args=(new_article.slug,)))	

def edit(request, slug):
	article = get_object_or_404(Article, slug=slug)
	context = {'article': article}
	return render(request, 'inj/edit.html', context)
	
def changearticle(request, slug):
	article = get_object_or_404(Article, slug=slug)
	try:
		article.article_content = request.POST['content']
		article.html_safe = request.POST['html-safe']
	except (KeyError):
		return render(request, 'inj/edit.html', {
			'article': article,
			'error_message': "Something didn't work somehow.",
		})
	else:
		article.save()
		return HttpResponseRedirect(reverse('inj:article', args=(article.slug,)))

