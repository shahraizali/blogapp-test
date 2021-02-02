from django.db import models

# Create your models here.
from blogProject.constants import ARTICLE_STATUS, ArticleStatus


class Article(models.Model):
    title = models.CharField(
        max_length=128,
    )
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=ARTICLE_STATUS, default=ArticleStatus.DRAFT)
    written_by = models.ForeignKey(
        "users.Writer",
        on_delete=models.SET_NULL,
        null=True,
        related_name="writer_articles",
    )
    edited_by = models.ForeignKey(
        "users.Writer",
        on_delete=models.SET_NULL,
        null=True,
        related_name="editor_articles",
    )
