import json
#from django.shortcuts import redirect
from django.http import StreamingHttpResponse, Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
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

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

UserModel = User()

class AuthArticle(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, article_id, format=None):
        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            raise Http404
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
        
    def put(self, request, article_id):
        payload = json.loads(request.body)
        try:
            article = Article.objects.filter(id=article_id)
            author = Author.objects.get(id=payload["author"])
            article.update(
                title=payload["title"],
                category=payload["category"],
                summary=payload["summary"], 
                firstParagraph=payload["firstParagraph"],
                body=payload["body"],
                author=author
            )
            new_article = Article.objects.get(id=article_id)
            serializer = ArticleSerializer(new_article)
            return Response({'Article': serializer.data},status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, article_id):
        try:
            article = Article.objects.get(id=article_id)
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        payload = json.loads(request.body)
        user = request.user
        try:
            author = Author.objects.get(id=payload["author"])
            article = Article.objects.create(
                title=payload["title"],
                category=payload["category"],
                summary=payload["summary"], 
                firstParagraph=payload["firstParagraph"],
                body=payload["body"],
                author=author
            )
            serializer = ArticleSerializer(article)
            return Response({'Articles': serializer.data},status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

##
##
## Author views
##
##

class AuthAuthor(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, author_id):
        payload = json.loads(request.body)
        try:
            author = Author.objects.filter(id=author_id)
            author.update(
                name=payload["name"],
                picture=payload["picture"]
            )
            new_author = Author.objects.get(id=author_id)
            serializer = AuthorSerializer(new_author)
            return Response({'Author': serializer.data},status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
            author.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        payload = json.loads(request.body)
        user = request.user
        try:
            author = Author.objects.create(
                name=payload["name"],
                picture=payload["picture"],
            )
            serializer = AuthorSerializer(author)
            return Response({'Author': serializer.data},status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

class CreateUserView(generics.CreateAPIView):
    model = UserModel
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer

##
##
## Article views
##
##

class ArticleList(generics.ListAPIView):
 authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]

 permission_classes = [
    permissions.AllowAny # Or anon users can't register
 ]
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
 authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]

 permission_classes = [
    permissions.AllowAny # Or anon users can't register
 ]

 def get(self, request, article_id, format=None):
  try:
    article = Article.objects.get(pk=article_id)
  except Article.DoesNotExist:
    raise Http404

  if request.user.is_authenticated is True:
      serializer = ArticleSerializer(article)
  else:
      serializer = ArticleBasicSerializer(article)

  return Response(serializer.data)

