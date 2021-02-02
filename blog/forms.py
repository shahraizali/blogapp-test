from django import forms
from django.core.exceptions import ValidationError

from blog.models import Article


class CreateArticleForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea())

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")
        if Article.objects.filter(title=title).count() > 0:
            raise ValidationError({"title": "This title already exists!"})


class UpdateArticleForm(forms.Form):
    id = forms.IntegerField(required=False)
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea())

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")
        id = cleaned_data.get("id")
        if id and Article.objects.filter(title=title).exclude(id=id).count() > 0:
            raise ValidationError({"title": "This title already exists!"})
