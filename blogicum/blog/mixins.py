from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from .forms import PostForm
from .models import Post

User = get_user_model()


class ProfileSuccessUrlMixin:
    model = Post
    template_name = "blog/create.html"

    def get_success_url(self):
        return reverse(
            "blog:profile", kwargs={"username": self.request.user.username}
        )


class AuthorRequiredAndPostSuccessUrlMixin(UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user == self.get_object().author
        )

    def get_success_url(self):
        return reverse(
            "blog:post_detail", args=[self.kwargs["post_id"]]
        )


class PostFormValidMixin:
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = get_object_or_404(
            User, username=self.request.user.username
        )
        return super().form_valid(form)


class DispatchAuthorMixin:
    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if request.user != post.author:
            return HttpResponseRedirect(
                reverse("blog:post_detail", kwargs={"post_id": post.id})
            )
        return super().dispatch(request, *args, **kwargs)
