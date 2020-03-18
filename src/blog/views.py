from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import User
from operator import attrgetter
from django.db.models import Q
from .models import Post

# Create your views here.
# CRUD
# Posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'post'
    ordering = ['-date_posted']
    paginate_by = 5

class SearchListView(ListView):
    model = Post
    template_name = 'blog/search_result.html'
    context_object_name = 'post'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        post = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context

class PostDetailView(DetailView):
    model = Post


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'body', 'post_pic']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'body', 'post_pic']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
# User Posts
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'post'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

#Search
def PostList(request):
    posts = Post.objects.all()
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(Q(title__icontains=query)|Q(body__icontains=query))

    context = {'posts': posts,}

    return render(request, 'blog/post_list.html', context)
