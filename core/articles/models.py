import uuid

from django.db import models
from django.urls import reverse


def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    name =filename.split('.')[0]
    filename = "{}.{}".format(name, ext.lower())

    return 'media/{sub}/{filename}'.format(
        sub=name,
        filename=filename
        )


class Category(models.Model):
    title = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('articles:category-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Article(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='article')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    description = models.TextField()
    content = models.TextField()
    add_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['add_date']

    def get_absolute_url(self):
        return reverse('articles:article-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='commentator')
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['add_time']

    def __str__(self):
        return self.content
