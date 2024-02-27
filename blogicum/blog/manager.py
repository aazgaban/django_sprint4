from django.db import models
from django.db.models import Count
from django.utils import timezone


class PostManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                pub_date__lte=timezone.now(),
                is_published=True,
                category__is_published=True,
            )
            .annotate(comment_count=Count("comments"))
            .order_by("-pub_date")
        )
