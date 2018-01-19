from django.urls import path

from . import views

app_name = 'news_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('article/<slug:slug>/<int:id>', views.detail, name='detail'),
    path('category/', views.categories_list, name='categories_list'),
    path('category/<str:category>/', views.category_articles, name='category_articles')
]