from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .forms import CommentForm, ArticleForm, CategoryForm
from .models import Article, Category, Comment


class ArticlesHome(ListView):
    context_object_name = 'articles-home'
    queryset = Article.objects.all()
    template_name = 'articles/articles_home.html'

    def get_context_data(self, **kwargs):
        context = super(ArticlesHome, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['articles_list'] = self.queryset
        return context


class CategoryDetail(DetailView):
    model = Category
    template_name = 'articles/category_detail.html'


class ArticleDetail(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm(initial={'article': self.object })
        context['comments'] = Comment.objects.filter(article=self.object)
        return context


class CreateComment(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse('articles:article-detail', kwargs={'pk': self.object.article_id})


class DeleteComment(DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('articles:article-detail', kwargs={'pk': self.object.article_id})


class CreateCategory(PermissionRequiredMixin, CreateView):
    permission_required = ("is_staff", "is_superuser",)
    model = Category
    form_class = CategoryForm
    template_name = 'crud/cr_upd_category.html'


class UpdateCategory(PermissionRequiredMixin, UpdateView):
    permission_required = ("is_staff", "is_superuser",)
    model = Category
    form_class = CategoryForm
    template_name = 'crud/cr_upd_category.html'

    def get_success_url(self):
        return reverse('articles:articles-home')


class DeleteCategory(PermissionRequiredMixin, DeleteView):
    permission_required = ("is_staff", "is_superuser",)
    model = Category
    template_name = 'crud/delete_category.html'

    def get_success_url(self):
        return reverse('articles:articles-home')


class CreateArticle(PermissionRequiredMixin, CreateView):
    permission_required = ("is_staff", "is_superuser")
    model = Article
    form_class = ArticleForm
    template_name = 'crud/cr_upd_article.html'


class UpdateArticle(PermissionRequiredMixin, UpdateView):
    permission_required = ("is_staff", "is_superuser",)
    model = Article
    form_class = ArticleForm
    template_name = 'crud/cr_upd_article.html'

    def get_success_url(self):
        article = self.get_object()
        return reverse('articles:article-detail', kwargs={'pk': article.pk})


class DeleteArticle(PermissionRequiredMixin, DeleteView):
    permission_required = ("is_staff", "is_superuser",)
    model = Article
    template_name = 'crud/delete_article.html'

    def get_success_url(self):
        return reverse('articles:articles-home')
