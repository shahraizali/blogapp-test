from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from blog.forms import CreateArticleForm, UpdateArticleForm
from blog.models import Article
from blogProject.constants import ArticleStatus
from users.models import Writer


class dashboardView(TemplateView):
    template_name = "dashboard/index.html"

    def get(self, request, *args, **kwargs):
        last_30_days = datetime.today() - timedelta(days=30)
        articles_thirty = Count(
            "writer_articles", filter=Q(writer_articles__created_at__gte=last_30_days)
        )
        articles_total = Count("writer_articles")
        writers = (
            Writer.objects.all()
            .annotate(articles_total=articles_total)
            .annotate(articles_thirty=articles_thirty)
        )
        context = {"writers": writers}
        return render(request, self.template_name, context)


class ArticleView(TemplateView):
    template_name = "blog/article_list.html"

    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        form = CreateArticleForm()
        context = {"articles": articles, "form": form}
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="/admin/login"))
    def post(self, request, *args, **kwargs):
        try:
            writer = request.user.writer_user
        except:
            return render(
                request,
                self.template_name,
                {"error": "Login with a user who is writer"},
            )
        form = CreateArticleForm(request.POST)
        success = False
        if form.is_valid():
            Article.objects.create(
                title=form.cleaned_data["title"],
                content=form.cleaned_data["content"],
                written_by=writer,
            )
            success = True
        articles = Article.objects.all()
        context = {"form": form, "articles": articles, "success": success}
        return render(request, self.template_name, context)


class ArticleDetailView(TemplateView):
    template_name = "blog/article_details.html"

    @method_decorator(login_required(login_url="/admin/login"))
    def get(self, request, *args, **kwargs):
        try:
            writer = request.user.writer_user
        except:
            return render(
                request,
                self.template_name,
                {"error": "Login with a user who is writer"},
            )
        try:
            article_id = kwargs["article_id"]
            article = Article.objects.get(id=article_id)
        except KeyError:
            return 404
        except Article.DoesNotExist:
            return 404
        except Article.MultipleObjectsReturned:
            return 404

        form = UpdateArticleForm(
            data={"title": article.title, "content": article.content}
        )
        context = {"article": article, "form": form, "is_editor": writer.is_editor}
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="/admin/login"))
    def post(self, request, *args, **kwargs):
        try:
            writer = request.user.writer_user
        except:
            return render(
                request,
                self.template_name,
                {"error": "Login with a user who is writer"},
            )
        article_id = kwargs["article_id"]
        data = request.POST.copy()
        data.update({"id": article_id})
        form = UpdateArticleForm(data)
        success = False
        if form.is_valid():
            Article.objects.filter(id=article_id).update(
                title=form.cleaned_data["title"],
                content=form.cleaned_data["content"],
                status=ArticleStatus.DRAFT,
            )
            success = True
        articles = Article.objects.all()
        context = {
            "form": form,
            "articles": articles,
            "is_editor": writer.is_editor,
            "success": success,
        }
        return render(request, self.template_name, context)


class ArticleApprove(TemplateView):
    template_name = "blog/article_approve.html"

    @method_decorator(login_required(login_url="/admin/login"))
    def get(self, request, *args, **kwargs):
        try:
            writer = request.user.writer_user
            if not writer.is_editor:
                return render(
                    request,
                    self.template_name,
                    {"error": "Login with a user who is editor"},
                )
        except:
            return render(
                request,
                self.template_name,
                {"error": "Login with a user who is writer"},
            )
        articles = Article.objects.filter(status=ArticleStatus.DRAFT)
        context = {"articles": articles}
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="/admin/login"))
    def post(self, request, *args, **kwargs):
        try:
            writer = request.user.writer_user
            if not writer.is_editor:
                return render(
                    request,
                    self.template_name,
                    {"error": "Login with a user who is editor"},
                )
        except:
            return render(
                request,
                self.template_name,
                {"error": "Login with a user who is writer"},
            )

        action = request.POST.get("action", None)
        article_id = request.POST.get("article_id", None)
        if action and article_id:
            if action == "approve":
                status = ArticleStatus.PUBLISHED
            elif action == "reject":
                status = ArticleStatus.REJECTED
            else:
                status = ArticleStatus.DRAFT
            article = Article.objects.filter(id=article_id).update(
                edited_by=writer, status=status
            )
        articles = Article.objects.filter(status=ArticleStatus.DRAFT)
        context = {"articles": articles}
        return render(request, self.template_name, context)


class ArticleEdited(TemplateView):
    template_name = "blog/article_edited.html"

    def get(self, request, *args, **kwargs):
        try:
            writer = request.user.writer_user
            if not writer.is_editor:
                return render(
                    request,
                    self.template_name,
                    {"error": "Login with a user who is editor"},
                )
        except:
            return render(
                request,
                self.template_name,
                {"error": "Login with a user who is writer"},
            )
        articles = Article.objects.filter(edited_by=writer)
        context = {"articles": articles}
        return render(request, self.template_name, context)
