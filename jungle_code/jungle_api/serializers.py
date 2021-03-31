from rest_framework import serializers
from jungle_api.models import Author, Article
from rest_framework.utils.urls import replace_query_param
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()

        token = Token.objects.create(user=user)
        token.save()

        return user

class AuthorSerializer(serializers.ModelSerializer):
 class Meta:
  model = Author	
  fields = ('id', 'name', 'picture')

class AuthorBasicSerializer(serializers.ModelSerializer):
 class Meta:
  model = Author	
  fields = ('id', 'name',)

class ArticleSerializer(serializers.ModelSerializer):
 class Meta:
  model = Article
  depth = 1
  fields = ('id', 'title','author','category','summary', 'firstParagraph', 'body')

class ArticleBasicSerializer(serializers.ModelSerializer):
 summary = serializers.CharField(max_length=200)
 class Meta:
  model = Article
  depth = 1
  fields = ('id', 'title','author','category','summary', 'firstParagraph')
