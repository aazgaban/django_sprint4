from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("posts/create/",
         views.PostCreateView.as_view(), name="create_post"),
    path("posts/<int:post_id>/",
         views.PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:post_id>/edit/",
         views.PostUpdateView.as_view(), name="edit_post"),
    path(
        "posts/<int:post_id>/delete/",
        views.PostDeleteView.as_view(),
        name="delete_post",
    ),
    path(
        "posts/<int:post_id>/comment/",
        views.AddCommentView.as_view(),
        name="add_comment",
    ),
    path(
        "posts/<int:post_id>/edit_comment/<int:comment_id>/",
        views.EditCommentView.as_view(),
        name="edit_comment",
    ),
    path(
        "posts/<int:post_id>/delete_comment/<int:comment_id>/",
        views.DeleteCommentView.as_view(),
        name="delete_comment",
    ),
    path(
        "category/<slug:category_slug>/",
        views.CategoryListView.as_view(),
        name="category_posts",
    ),
    path(
        "profile/<slug:username>/",
        views.ProfileDetailView.as_view(),
        name="profile"
    ),
    path(
        "edit/",
        views.ProfileUpdateView.as_view(),
        name="edit_profile"
    ),
    path("",
         views.PostListView.as_view(),
         name="index"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)