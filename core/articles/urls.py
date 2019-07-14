from django.urls import path, include
from rest_framework import routers

from .views import ArticlesHome, CategoryDetail, ArticleDetail, CreateComment, DeleteComment, CreateArticle, \
    UpdateArticle, DeleteArticle, DeleteCategory, UpdateCategory, CreateCategory
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
    path('comment/delete/<int:pk>', DeleteComment.as_view(), name='delete-comment'),

    path('category/create/', CreateCategory.as_view(), name='category-create'),
    path('category/<int:pk>/update/', UpdateCategory.as_view(), name='category-update'),
    path('category/<int:pk>/delete/', DeleteCategory.as_view(), name='category-delete'),
    path('article/create/', CreateArticle.as_view(), name='article-create'),
    path('article/<int:pk>/update/', UpdateArticle.as_view(), name='article-update'),
    path('article/<int:pk>/delete/', DeleteArticle.as_view(), name='article-delete'),

]
