from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from jungle_api import views
from django.conf.urls import url, include
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token 

urlpatterns = [
 url(r'^sign-up/$', views.CreateUserView.as_view()),
 path('login/', obtain_auth_token, name='api_token_auth'),
 url(r'^admin/articles/$', views.AuthArticle.as_view()),
 url(r'^admin/articles/(?P<article_id>[0-9]+)', views.AuthArticle.as_view()),
 url(r'^admin/authors/$', views.AuthAuthor.as_view()),
 url(r'^admin/authors/(?P<author_id>[0-9]+)', views.AuthAuthor.as_view()),
 url(r'^articles/$', views.ArticleList.as_view()),
 url(r'^articles/(?P<article_id>[0-9]+)/$', views.ArticleDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)