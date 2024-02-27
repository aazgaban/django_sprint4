from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CommentForm, PostForm, ProfileForm
from .models import Category, Comment, Post, User
from blogicum.constants import PAGE_NUM


class SuccessUrlMixin:
    def get_success_url(self):
        return reverse("blog:profile",
                       kwargs={"username": self.request.user.username})


class СommentSuccessUrlMixin:
    def dispatch(self, request, *args, **kwargs):
        if (
                not request.user.is_authenticated
                or request.user != self.get_object().author
        ):
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("blog:post_detail", args=[self.kwargs["post_id"]])


class DispatchNotAuthMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class DispatchAuthorMixin:
    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if request.user != post.author:
            return HttpResponseRedirect(
                reverse_lazy("blog:post_detail", kwargs={"post_id": post.id})
            )
        return super().dispatch(request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post
    form_class = CommentForm
    template_name = "blog/detail.html"
    pk_url_kwarg = "post_id"

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["comments"] = Comment.objects.filter(
            post=self.kwargs["post_id"]
        ).order_by("created_at")
        return context

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if not post.is_published and request.user != post.author:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class PostListView(ListView):
    model = Post
    paginate_by = PAGE_NUM
    template_name = "blog/index.html"

    def get_queryset(self):
        return Post.is_pub.prefetch_related("category", "location", "author")


class PostCreateView(
    DispatchNotAuthMixin, SuccessUrlMixin, CreateView, LoginRequiredMixin
):
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(
    DispatchAuthorMixin, SuccessUrlMixin, UpdateView, LoginRequiredMixin
):
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"
    pk_url_kwarg = "post_id"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(
    DispatchAuthorMixin, SuccessUrlMixin, DeleteView, LoginRequiredMixin
):
    model = Post
    template_name = "blog/create.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Post, id=self.kwargs.get("post_id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        context["form"] = PostForm(instance=instance)
        return context


class ProfileDetailView(ListView):
    model = User
    template_name = "blog/profile.html"
    paginate_by = PAGE_NUM

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs["username"])

    def get_queryset(self):
        query_set = (
            Post.objects.filter(author__username=self.kwargs["username"])
            .annotate(comment_count=Count("comments"))
            .order_by("-pub_date")
        )
        if (
                self.request.user.is_authenticated
                and self.request.user == self.get_object()
        ):
            return query_set
        else:
            return Post.is_pub.filter(author__username=self.kwargs["username"])

    def get_context_data(self, **kwargs):
        return dict(**super().get_context_data(**kwargs),
                    profile=self.get_object())


class ProfileUpdateView(
    DispatchNotAuthMixin, SuccessUrlMixin, UpdateView, LoginRequiredMixin
):
    model = User
    form_class = ProfileForm
    template_name = "blog/user.html"

    def get_object(self, queryset=None):
        return self.request.user


class CategoryListView(ListView):
    model = Post
    template_name = "blog/category.html"
    paginate_by = PAGE_NUM

    def get_queryset(self):
        query_set = Post.is_pub.filter(
            category__slug=self.kwargs["category_slug"])
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category,
                                     slug=self.kwargs["category_slug"])
        if not category.is_published:
            raise Http404()
        context["category"] = category
        return context


class AddCommentView(DispatchNotAuthMixin, CreateView, LoginRequiredMixin):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment.html"

    def form_valid(self, form):
        post_id = self.kwargs["post_id"]
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=post_id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post_detail", args=[self.kwargs["post_id"]])


class EditCommentView(СommentSuccessUrlMixin, UpdateView, LoginRequiredMixin):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment.html"
    pk_url_kwarg = "comment_id"


class DeleteCommentView(СommentSuccessUrlMixin, DeleteView,
                        LoginRequiredMixin):
    model = Comment
    template_name = "blog/comment.html"

    def get_object(self, queryset=None):
        post_id = self.kwargs.get("post_id")
        comment_id = self.kwargs.get("comment_id")
        return get_object_or_404(Comment, id=comment_id, post=post_id)
