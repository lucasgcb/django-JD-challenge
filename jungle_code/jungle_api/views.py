import json
#from django.shortcuts import redirect
from django.http import StreamingHttpResponse, Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from jungle_api.models import Author,Article
from jungle_api.serializers import AuthorBasicSerializer,AuthorSerializer,ArticleSerializer,ArticleBasicSerializer, UserSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from rest_framework import viewsets  
from rest_framework import generics
from rest_framework import permissions
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

UserModel = User()

class LoginView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)

##
##
## Author views
##
##


class CreateUserView(generics.CreateAPIView):
    model = UserModel
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer



@api_view(['GET'])
def author_list(request, format=None):
    if request.method == 'GET':
        authors = Author.objects.all()
        serializer = AuthorBasicSerializer(authors, many=True)
        return StreamingHttpResponse(json.dumps(serializer.data, sort_keys=True, indent=4, separators=(',', ': ')), content_type='application/json')

@api_view(['GET'])
def author_detail(request, pk, format=None):
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AuthorBasicSerializer(author)
        return StreamingHttpResponse(json.dumps(serializer.data, sort_keys=True, indent=4, separators=(',', ': ')), content_type='application/json')
##
##
## Article views
##
##

class ArticleList(generics.ListAPIView):
 queryset = Article.objects.all()
 serializer_class = ArticleBasicSerializer
 def get_queryset(self):
        queryset = Article.objects.all().order_by('-id')
        category = self.request.query_params.get('category', None)
        if category is not None:
         try:
          queryset = queryset.filter(category=category)
         except ValueError:
          queryset = Article.objects.all().order_by('-id')
        return queryset

class ArticleDetail(APIView):
 def get_object(self, pk):
  try:
    return Article.objects.get(pk=pk)
  except Author.DoesNotExist:
    raise Http404

 def get(self, request, pk, format=None):
  article = self.get_object(pk)
  serializer = ArticleBasicSerializer(article)
  return Response(serializer.data)

