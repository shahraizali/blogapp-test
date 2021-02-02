from django.urls import path

from blog.views import ArticleView, ArticleDetailView, ArticleApprove, ArticleEdited

urlpatterns = [
    path("article/", ArticleView.as_view(), name="article_listing"),
    path(
        "article/<int:article_id>/", ArticleDetailView.as_view(), name="article_detail"
    ),
    path("article-approval/", ArticleApprove.as_view(), name="article_approve"),
    path("articles-edited/", ArticleEdited.as_view(), name="article_edited"),
]
