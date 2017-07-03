from django.conf.urls import url
from django.contrib.auth import views as auth_views
from registration.backends.hmac.views import RegistrationView
from .forms import UserFormNames

from . import views

app_name = 'inj'
urlpatterns = [
	url(r'^$', views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'inj/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^register/$',
        RegistrationView.as_view(
            form_class=UserFormNames
        ),
        name='registration_register',
    ),
	url(r'^newarticle/(?P<slug>[\w-]+)/$', views.newarticle, name='newarticle'),
	url(r'^addarticle/$', views.addarticle, name='addarticle'),
	url(r'^addarticle/(?P<slug>[\w-]+)/$', views.addarticle, name='addarticle'),
	url(r'^articles-by-date/$', views.articlesbydate, name='articlesbydate'),
	url(r'^comments-by-date/$', views.commentsbydate, name='commentsbydate'),
	url(r'^userpage/(?P<username>[\w-]+)/$', views.userpage, name='userpage'),
	url(r'^(?P<slug>[\w-]+)/$', views.article, name='article'),
	url(r'^(?P<slug>[\w-]+)/addcomment/$', views.addcomment, name='addcomment'),
	url(r'^(?P<slug>[\w-]+)/edit/$', views.edit, name='edit'),
	url(r'^(?P<slug>[\w-]+)/changearticle/$', views.changearticle, name='changearticle'),
	url(r'^(?P<slug>[\w-]+)/delete/$', views.delete, name='delete'),

]