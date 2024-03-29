from blog.models import Category, Comment, Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CommentForm, PostForm, UserProfileForm

app_name = 'blog'


class CategoryPostListView(ListView):
    template_name = 'blog/category.html'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category,
                                          slug=self.kwargs['slug'],
                                          is_published=True)
        return Post.objects.get_filter_for_post().filter(
            category=self.category,
            category__is_published=True).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProfileView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile'
    paginate_by = 10

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(author=context['profile'])
        paginator = Paginator(posts, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:profile')

    def get_success_url(self):
        username = self.request.user.username
        return reverse('blog:profile', args=[username])

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(User, pk=kwargs['pk'])
        if instance.username != request.user.username:
            return redirect('registration')
        return super().dispatch(request, *args, **kwargs)


class PostListView(ListView):
    model = Post
    queryset = Post.objects.get_filter_for_post().filter(
        category__is_published=True).order_by('-pub_date')
    paginate_by = 10
    template_name = 'blog/index.html'


class PostDetailView(DetailView):
    model = Post
    form_class = PostForm
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post.objects.all(),
                                 id=self.kwargs['id'])
        context['post'] = post
        context['form'] = CommentForm()
        context['comments'] = (self.object.comment.select_related('author'))
        return context


class BaseMixin:
    def dispatch(self, request, *args, **kwargs):
        if isinstance(self, PostMixin):
            instance = get_object_or_404(Post, id=kwargs['post_id'])
            if instance.author != request.user:
                return redirect('blog:post_detail', id=kwargs['post_id'])
            return super().dispatch(request, *args, **kwargs)
        elif isinstance(self, CommentMixin):
            comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
            if comment.author != request.user:
                return redirect('registration')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        username = self.request.user.username
        return reverse('blog:profile', args=[username])


class PostMixin(BaseMixin):
    pass


class CommentMixin(BaseMixin):
    pass


class PostValidMixin:
    def form_valid(self, form):
        form.instance.author = self.request.user
        if not form.instance.pub_date:
            form.instance.pub_date = timezone.now()
        return super().form_valid(form)


class PostCreateView(PostValidMixin, LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        username = self.request.user.username
        return reverse('blog:profile', args=[username])


class PostUpdateView(PostMixin,
                     PostValidMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'


class PostDeleteView(PostMixin,
                     PostValidMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'


class CommentCreateView(LoginRequiredMixin, CreateView):
    posts = None
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        self.posts = get_object_or_404(Post, id=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.post = self.posts
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'id': self.posts.pk})


class CommentDeleteView(CommentMixin, LoginRequiredMixin, DeleteView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'


class CommentUpdateView(CommentMixin, LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
