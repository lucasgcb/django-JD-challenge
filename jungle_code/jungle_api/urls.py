from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from jungle_api import views
from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token 

urlpatterns = [
 url(r'^sign-up/$', views.CreateUserView.as_view()),
 url(r'^login/$', views.LoginView.as_view()), 
 url(r'^authors/$', views.author_list),
 url(r'^authors/(?P<pk>[0-9]+)/$', views.author_detail),
 url(r'^articles/$', views.ArticleList.as_view()),
 url(r'^articles/(?P<pk>[0-9]+)/$', views.ArticleDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)