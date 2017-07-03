from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.urls import reverse
from django.views import generic
from django.db import IntegrityError
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import UserFormNames
from registration.signals import user_registered

from .models import Article, Commentary

import urllib2
import json

def index(request):
	return HttpResponseRedirect(reverse('inj:article', args=('welcome',)))

def getchart():
	chart = getmaincats()
	context = {
		'chart': chart,
	}
	return context

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
	list_link += '<div class="chart-item"><a href="../' + article.slug + '">' + article.title + '</a></div></li>'
	return list_link
	
def is_visible(title, show):
	html = '<ul class="chart'
	article = Article.objects.get(title=title)
	if show == False: html += ' hidden'
	html += '">'	
	return html
	
def home(request):
	latest_articles = Article.objects.order_by('-pub_date')[:5]
	latest_comments = Commentary.objects.order_by('-pub_date')[:5]
	context = getchart()
	context['latest_articles'] = latest_articles
	context['latest_comments'] = latest_comments
	return render(request, 'inj/home.html', context)
	
def article(request, slug):
	article = ""
	try:
		article = Article.objects.get(slug=slug)
	except ObjectDoesNotExist:
		return HttpResponseRedirect(reverse('inj:home'))
	context = getchart()
	context['article'] = article
	context['breadcrumbs'] = getbreadcrumbs(slug)
	user_auth = request.user.is_authenticated()
	context['user_auth'] = user_auth
	if article.comments:
		return render(request, 'inj/article.html', context)
	else:
		return render(request, 'inj/article-main.html', context)

def getbreadcrumbs(slug):
	breadcrumbs = '<p>'
	parent = Article.objects.get(slug=slug).parent
	if parent:
		parent_list = [parent.title]
		add_parent_to_list(parent_list)
		parent_list.reverse()
		for i in range(len(parent_list)):
			article = Article.objects.get(title=parent_list[i])
			breadcrumbs += '<a href="../' + article.slug + '">' + article.title + '</a> -> '
	breadcrumbs += '</p>'
	return breadcrumbs

def add_parent_to_list(parent_list):
	parent = Article.objects.get(title=parent_list[-1]).parent
	if parent:
		parent_list.append(parent.title)
		add_parent_to_list(parent_list)
	return parent_list

def addcomment(request, slug):
	article = get_object_or_404(Article, slug=slug)
	com = article.commentary_set
	com_title = request.POST['title']
	com_author = request.POST['author']
	commentary = request.POST['comment']
	recaptcha_response = request.POST['g-recaptcha-response']	
	if reCAPTCHA(recaptcha_response)==False:
		return render(request, 'inj/article.html', {
		'article': article,
		'error_message': "You failed the reCAPTCHA test. Please try again."
	})
	if commentary != "" and commentary != "Please type or paste your text here.":
		com.create(com_title=com_title, com_author=com_author, commentary=commentary)
		return HttpResponseRedirect(reverse('inj:article', args=(article.slug,)))
	else:
		return render(request, 'inj/article.html', {
		'article': article,
		'error_message': "That wasn't a valid comment. Please try again.",
		})
		
def reCAPTCHA(response):
	secret = '6LeV_yMUAAAAANIIN0404-FDoi-fPvxmCYLSCEMQ'
	url = 'https://www.google.com/recaptcha/api/siteverify' + '?secret=' + secret + '&response=' + response
	g = urllib2.urlopen(url)
	google_verify = json.loads(g.read())
	return google_verify['success']
				
def articlesbydate(request):
	context = getchart()
	list_all = Article.objects.order_by('-pub_date')
	context['article_list'] = list_all
	return render(request, 'inj/articles-by-date.html', context)

def commentsbydate(request):
	context = getchart()
	list_all = Commentary.objects.order_by('-pub_date')
	context['comment_list'] = list_all
	return render(request, 'inj/comments-by-date.html', context)

@login_required		
def newarticle(request, slug):
	context = {
		'articles': Article.objects.all().order_by('title'),
	}
	if slug != "None":
		context['parent'] = Article.objects.get(slug=slug)
	return render(request, 'inj/newarticle.html', context)

def addarticle(request):
	title = ""
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
		new_article.contributor = request.user
		new_article.article_content = request.POST['content']	
		new_article.html_safe = request.POST['html-safe']
		parent = Article.objects.get(title=request.POST['parent'])	
		new_article.parent = parent
		new_article.save()		
		return HttpResponseRedirect(reverse('inj:article', args=(new_article.slug,)))	

@login_required
def edit(request, slug):
	article = get_object_or_404(Article, slug=slug)
	context = {'article': article}
	return render(request, 'inj/edit.html', context)
	
def changearticle(request, slug):
	article = get_object_or_404(Article, slug=slug)
	try:
		article.article_content = request.POST['content']
		article.html_safe = request.POST['html-safe']
		article.save()
	except (KeyError):
		return render(request, 'inj/edit.html', {
			'article': article,
			'error_message': "Something didn't work somehow.",
		})
	else:
		return HttpResponseRedirect(reverse('inj:article', args=(article.slug,)))

def userpage(request, username):
	contributor = User.objects.get(username=username)
	articles = Article.objects.filter(contributor=contributor).order_by('-pub_date')
	user_auth = request.user.is_authenticated()
	context = {
		'contributor': contributor,
		'articles': articles,
		'user_auth': user_auth,
	}
	return render(request, 'inj/userpage.html', context)
	
def user_created(sender, user, request, **kwargs):
    form = UserFormNames(request.POST)
    # Update first and last name for user
    user.first_name=form.data['first_name']
    user.last_name=form.data['last_name']
    user.save()
    
user_registered.connect(user_created)

@login_required
def delete(request, slug):
	article = get_object_or_404(Article, slug=slug)
	if request.method == 'POST':
		title = article.title	
		article.delete()
		return HttpResponseRedirect(reverse('inj:userpage', args=(request.user.username,)))
	else:
		context = {'article': article}
		return render(request, 'inj/delete.html', context)
	