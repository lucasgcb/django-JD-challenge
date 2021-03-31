import os
import re
from django.db import models
from django.db.models.signals import pre_delete
from django.core.exceptions import SuspiciousFileOperation
from django.dispatch import receiver
from django.contrib.auth.models import User
from string import Template

class Author(models.Model):
  name = models.CharField(max_length=100, blank=False, default='')
  picture = models.URLField(max_length=200)
  def __str__(self):
   return '%s' % (self.name)
   
   
class Article(models.Model):
  title = models.CharField(max_length=200, blank=False, default='')
  author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=False)
  category = models.CharField(max_length=200, blank=False, default='')
  summary = models.CharField(max_length=200, blank=False, default='')
  firstParagraph = models.CharField(max_length=200, blank=False, default='')
  body = models.CharField(max_length=2000, blank=False, default='')
  def __str__(self):
   return 'ID: %s | Title: %s | Author: %s | Category: %s ' % (self.id, self.title, self.author.name, self.category)

