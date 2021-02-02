from django.urls import path, include
from rest_framework.routers import DefaultRouter

from blog.api.v1 import api
from blog.api.v1.viewset import ArticleViewSet

router = DefaultRouter()
router.register("article", ArticleViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("article-approval/", api.ArticleApproval.as_view(), name="ArticleApproval"),
    path("articles-edited/", api.ArticleEdited.as_view(), name="ArticleApproval"),
]
