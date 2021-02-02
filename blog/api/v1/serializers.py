from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from blog.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = (
            "status",
            "written_by",
            "edited_by",
        )


class ArticleApprovalSerializer(serializers.Serializer):
    article_id = serializers.IntegerField()
    action = serializers.CharField()

    def validate(self, attrs):
        if attrs["action"] not in ["approved", "rejected"]:
            raise ValidationError(
                {"action": "action can be either 'approved' or 'rejected' "}
            )
        if Article.objects.filter(id=attrs["article_id"]).count() < 1:
            raise ValidationError({"article_id": "Invalid article_id "})
        return attrs
