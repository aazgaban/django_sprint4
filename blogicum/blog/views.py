from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blogicum.constants import PAGE_NUM
from .forms import CommentForm, PostForm, ProfileForm
from .mixins import (AuthorRequiredAndPostSuccessUrlMixin, DispatchAuthorMixin,
                     PostFormValidMixin, ProfileSuccessUrlMixin)
from .models import Category, Comment, Post, User


class PostDetailView(
    DetailView,
    LoginRequiredMixin
):
    form_class = CommentForm
    template_name = "blog/detail.html"

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            return get_object_or_404(
                Post,
                Q(id=self.kwargs.get("post_id"))
                & (Q(author=self.request.user) | Q(is_published=True))
            )
        else:
            return get_object_or_404(
                Post,
                Q(id=self.kwargs.get("post_id"), is_published=True)
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["comments"] = self.get_object().comments.order_by("created_at")
        return context


class PostListView(
    ListView
):
    model = Post
    paginate_by = PAGE_NUM
    template_name = "blog/index.html"

    def get_queryset(self):
        return Post.published_posts.prefetch_related(
            "category",
            "location",
            "author"
        )


class PostCreateView(
    LoginRequiredMixin,
    PostFormValidMixin,
    ProfileSuccessUrlMixin,
    CreateView
):
    form_class = PostForm


class PostUpdateView(
    DispatchAuthorMixin,
    PostFormValidMixin,
    ProfileSuccessUrlMixin,
    UpdateView,
    LoginRequiredMixin
):
    pk_url_kwarg = "post_id"


class PostDeleteView(
    DispatchAuthorMixin,
    ProfileSuccessUrlMixin,
    DeleteView,
    LoginRequiredMixin
):

    def get_object(self, queryset=None):
        return get_object_or_404(
            Post,
            id=self.kwargs.get("post_id")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = get_object_or_404(
            Post,
            pk=self.kwargs.get("post_id")
        )
        context["form"] = PostForm(instance=instance)
        return context


class ProfileDetailView(ListView):
    model = User
    template_name = "blog/profile.html"
    paginate_by = PAGE_NUM

    def get_object(self):
        return get_object_or_404(
            User,
            username=self.kwargs["username"]
        )

    def get_queryset(self):
        username = self.kwargs["username"]
        query_set = (
            Post.objects.filter(Q(author__username=username))
            .annotate(comment_count=Count("comments"))
            .order_by("-pub_date")
        )
        if (
                self.request.user.is_authenticated
                and self.request.user == self.get_object()
        ):
            return query_set
        else:
            return Post.published_posts.filter(
                Q(author__username=username)
            )

    def get_context_data(self, **kwargs):
        return dict(
            **super()
            .get_context_data(**kwargs),
            profile=self.get_object()
        )


class ProfileUpdateView(ProfileSuccessUrlMixin, UpdateView,
                        LoginRequiredMixin):
    model = User
    form_class = ProfileForm
    template_name = "blog/user.html"

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            return self.request.user


class CategoryListView(ListView):
    model = Post
    template_name = "blog/category.html"
    paginate_by = PAGE_NUM

    def get_queryset(self):
        query_set = Post.published_posts.filter(
            category__slug=self.kwargs["category_slug"]
        )
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(
            Category,
            Q(slug=self.kwargs["category_slug"]) & Q(is_published=True)
        )
        context["category"] = category
        return context


class AddCommentView(CreateView, LoginRequiredMixin):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment.html"

    def form_valid(self, form):
        post_id = self.kwargs["post_id"]
        form.instance.author = get_object_or_404(
            User,
            username=self.request.user.username
        )
        form.instance.post = get_object_or_404(
            Post,
            pk=post_id
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "blog:post_detail",
            args=[self.kwargs["post_id"]]
        )


class EditCommentView(
    AuthorRequiredAndPostSuccessUrlMixin,
    UpdateView,
    LoginRequiredMixin
):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment.html"
    pk_url_kwarg = "comment_id"


class DeleteCommentView(
    AuthorRequiredAndPostSuccessUrlMixin,
    DeleteView,
    LoginRequiredMixin
):
    model = Comment
    template_name = "blog/comment.html"

    def get_object(self, queryset=None):
        post_id = self.kwargs.get("post_id")
        comment_id = self.kwargs.get("comment_id")
        return get_object_or_404(
            Comment,
            id=comment_id,
            post=post_id
        )
