import json
#from django.shortcuts import redirect
from django.http import StreamingHttpResponse, Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from jungle_api.models import Author,Article
from jungle_api.serializers import AuthorBasicSerializer,AuthorSerializer,ArticleSerializer,ArticleBasicSerializer, UserSerializer
from django.shortcuts import render
from rest_framework import viewsets  
from rest_framework import generics
from rest_framework import permissions
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

UserModel = User()

class AuthArticleCreate(APIView):
    """
    Authenticated API View for the Article Create operation.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        """
        Create an article.

        Required fields:

        title - string,

        category - string,

        summary - string, 

        firstParagraph - string,
        
        body - string,

        author - int (author_id)

        Try /api/articles/ for the full list of articles.
        """
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
            return Response({'error': "Author with id  " + str(payload["author"]) + " does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            return Response({'error': "Missing fields: " + str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)
        

class AuthArticle(APIView):
    """
    Authenticated API View for Article Read, Update, and Delete operations.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, article_id):
        """
        Get a specific article from its article_id.

        Try /api/articles/ for the full list of articles.
        """
        try:
            article = Article.objects.get(pk=article_id)
            serializer = ArticleSerializer(article)
            return Response(serializer.data)
        except Article.DoesNotExist:
            raise Http404

    def delete(self, request, article_id):
        """
        Delete a specific article with the given article_id.

        Try /api/articles/ for the full list of articles.
        """
        try:
            article = Article.objects.get(id=article_id)
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self, request, article_id):
        """
        Update a specific article from its article_id.

        Try /api/articles/ for the full list of articles.
        """
        try:
            payload = json.loads(request.body)
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


##
##
## Author views
##
##


class AuthAuthorCreate(APIView):
    """
    Authenticated API View for Author Create operation.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        """
        Create an author.

        name - String
        picture - URL
        """
        try:
            payload = json.loads(request.body)
            author = Author.objects.create(
                name=payload["name"],
                picture=payload["picture"],
            )
            serializer = AuthorSerializer(author)
            return Response({'Author': serializer.data},status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)


class AuthAuthor(APIView):
    """
    Authenticated API View for Author Read, Update, and Delete operations.

    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id):
        """
        Get a specific author from their author_id.

        Requires author_id.
        """
        try:
            author = Author.objects.get(pk=author_id)
            serializer = AuthorSerializer(author)
            return Response(serializer.data)
        except Article.DoesNotExist:
            raise Http404

    def put(self, request, author_id):
        """
        Update a specific author from their author_id.

        Requires author_id.
        """
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
        """
        Delete a specific author with the given author_id.

        Requires author_id.
        """
        try:
            author = Author.objects.get(id=author_id)
            author.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

class CreateUserView(generics.CreateAPIView):
    """
    Create a user.

    Signs up an user.
    """
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
    """
    Get all articles from the database.

    Allows for the retrieval of articles filteres by category (/?category=:slug)

    Does not show body.
    """
    authentication_classes = [TokenAuthentication]

    permission_classes = [permissions.AllowAny]
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
    """
    Shows the article with the given article_id.

    Will only show body to authenticated users.
    """
    authentication_classes = [TokenAuthentication]

    permission_classes = [permissions.AllowAny]

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

