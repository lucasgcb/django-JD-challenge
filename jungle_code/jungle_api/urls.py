from rest_framework.urlpatterns import format_suffix_patterns
from jungle_api import views
from django.conf.urls import url, include
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token 
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^sign-up/$', views.CreateUserView.as_view()),
    path('login/', obtain_auth_token, name='api_token_auth'),
    url(r'^admin/articles/$', views.AuthArticleCreate.as_view()),
    url(r'^admin/articles/(?P<article_id>[0-9]+)/$', views.AuthArticle.as_view()),
    url(r'^admin/authors/$', views.AuthAuthorCreate.as_view()),
    url(r'^admin/authors/(?P<author_id>[0-9]+)/$', views.AuthAuthor.as_view()),
    url(r'^articles/$', views.ArticleList.as_view()),
    url(r'^articles/(?P<article_id>[0-9]+)/$', views.ArticleDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)