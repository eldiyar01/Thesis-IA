from rest_framework import serializers

from .models import Category, Article, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['pk', 'title']


class ArticleSerializer(serializers.ModelSerializer):
    # category = serializers.StringRelatedField(many=False)
    comments = serializers.StringRelatedField(many=True)

    class Meta:
        model = Article
        fields = ['pk', 'add_date', 'title', 'category', 'description', 'content', 'comments']


class CommentSerializer(serializers.ModelSerializer):
    # article = serializers.StringRelatedField(many=True)
    user = serializers.StringRelatedField(many=False)

    class Meta:
        model = Comment
        fields = ['pk', 'add_time', 'article', 'user', 'content']

