from django.shortcuts import render
from django.http import HttpResponse

from .models import Article, Category, DataMine

def index(request):
  # modify this to return the most recent 5 articles
  # in ALL categories
  articles = Article.objects.all
  context = {'articles': articles}
  return render(request, 'news_app/index.html', context)

def detail(request, slug, id):
  article = None
  # try:
  article = Article.objects.get(pk=id)
  context = {'article': article}
  return render(request, 'news_app/detail.html', context )

def categories_list(request):
  all_categories = Category.objects.all()
  context = {'categories': all_categories}
  return render(request, 'news_app/categories_list.html', context)

def category_articles(request, category):
  articles_for_category = Article.objects.filter(category__name=category)
  context = {'articles': articles_for_category}

  return render(request, 'news_app/category_articles.html', context)
