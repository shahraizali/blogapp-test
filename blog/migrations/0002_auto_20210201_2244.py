# Generated by Django 3.1.6 on 2021-02-01 22:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_auto_20210201_2103"),
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="edited_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="editor_articles",
                to="users.writer",
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="written_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="writer_articles",
                to="users.writer",
            ),
        ),
    ]
