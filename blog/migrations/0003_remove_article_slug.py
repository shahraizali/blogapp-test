# Generated by Django 3.1.6 on 2021-02-01 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_auto_20210201_2244"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="article",
            name="slug",
        ),
    ]
