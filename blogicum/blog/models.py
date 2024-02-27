from blog.manager import PostManager
from core.models import BlogBaseModel
from django.contrib.auth import get_user_model
from django.db import models

from blogicum.constants import MAX_LENGTH, TITLE

User = get_user_model()


class Category(BlogBaseModel):
    title = models.CharField(TITLE, max_length=MAX_LENGTH)
    description = models.TextField("Описание")
    slug = models.SlugField(
        "Идентификатор",
        unique=True,
        help_text="Идентификатор страницы для URL; разрешены символы латиницы,"
                  " цифры, дефис и подчёркивание.",
    )

    class Meta(BlogBaseModel.Meta):
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.title[:MAX_LENGTH]} | {self.description} | {self.slug}"


class Location(BlogBaseModel):
    name = models.CharField("Название места", max_length=MAX_LENGTH)

    class Meta(BlogBaseModel.Meta):
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return f"{self.name[:MAX_LENGTH]}"


class Post(BlogBaseModel):
    title = models.CharField(TITLE, max_length=MAX_LENGTH)
    text = models.TextField("Текст")
    pub_date = models.DateTimeField(
        "Дата и время публикации",
        help_text="Если установить дату и время в будущем — можно делать"
                  " отложенные публикации.",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор публикации",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name="posts",
        null=True,
        verbose_name="Местоположение",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="posts",
        null=True,
        verbose_name="Категория",
    )
    image = models.ImageField("Фото", upload_to="posts_images", blank=True)
    objects = models.Manager()
    is_pub = PostManager()

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ["-pub_date"]

    def __str__(self):
        return f"{self.title[:MAX_LENGTH]} | {self.text}"



class Comment(models.Model):
    text = models.TextField("Комментарии")
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
