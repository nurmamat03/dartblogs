from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *
from django.db.models import F


class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мой первый блог'
        return context


class PostByCategory(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 1
    allow_empty = False

    def get_queryset(self):
        return Post.object.filter(category_slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category, object.filter(category_slug=self.kwargs['slug'])
        return context


class PostByTag(ListView):
    pass


class GetPost(DetailView):
    model = Post
    template_name = 'blog/search.html'
    context_object_name = 'posts'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


class Search(ListView):
    template_name = 'blog/single.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.filter(title_icontains=self.request.GET.get('set'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s{self.request.GET.get('s')}&"
        return context
