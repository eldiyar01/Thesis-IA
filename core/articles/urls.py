from django.urls import path, include
from rest_framework import routers

from .views import ArticlesHome, CategoryDetail, ArticleDetail, CreateComment, DeleteComment
from .viewsets import CategoryViewSet, ArticleViewSet, CommentViewSet

router = routers.SimpleRouter()
router.register('categories', CategoryViewSet)
router.register('articles', ArticleViewSet)
router.register('comments', CommentViewSet)


app_name = 'articles'
urlpatterns = [
    path('api/', include(router.urls)),

    path('', ArticlesHome.as_view(), name='articles-home'),
    path('category-detail/<int:pk>', CategoryDetail.as_view(), name='category-detail'),
    path('article-detail/<int:pk>', ArticleDetail.as_view(), name='article-detail'),
    path('comment/create/', CreateComment.as_view(), name='create-comment'),
    path('comment/delete/<int:pk>', DeleteComment.as_view(), name='delete-comment')
]