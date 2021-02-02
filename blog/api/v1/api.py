from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from blog.api.v1.permissions import IsEditor
from blog.api.v1.serializers import ArticleApprovalSerializer, ArticleSerializer
from blog.models import Article
from blogProject.constants import ArticleStatus


class ArticleApproval(GenericAPIView):
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [IsAuthenticated, IsEditor]
    serializer_class = ArticleApprovalSerializer

    def post(self, request):
        serializer = ArticleApprovalSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            article_id = serializer.data["article_id"]
            action = serializer.data["action"]
            if action == "approved":
                article_status = ArticleStatus.PUBLISHED
            elif action == "rejected":
                article_status = ArticleStatus.REJECTED
            else:
                article_status = ArticleStatus.DRAFT
            Article.objects.filter(id=article_id).update(
                edited_by=request.user.writer_user, status=article_status
            )
        return Response(
            {"success": True, "result": serializer.data}, status.HTTP_200_OK
        )


class ArticleEdited(GenericAPIView):
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [IsAuthenticated, IsEditor]
    serializer_class = ArticleSerializer

    def get(self, request):
        articles = Article.objects.filter(edited_by=request.user.writer_user)
        serializer = ArticleSerializer(articles, many=True)
        return Response(
            {"success": True, "result": serializer.data}, status.HTTP_200_OK
        )
