from django.urls import path

from .views import NewsHome, CategoryDetail, NewsDetail

app_name = 'news'
urlpatterns = [
    path('', NewsHome.as_view(), name='news-home'),
    path('category-detail/<int:pk>', CategoryDetail.as_view(), name='category-detail'),
    path('news-detail/<int:pk>', NewsDetail.as_view(), name='news-detail'),
]