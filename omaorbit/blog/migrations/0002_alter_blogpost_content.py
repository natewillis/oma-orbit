# Generated by Django 5.2.3 on 2025-06-20 21:34

import markdownx.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='content',
            field=markdownx.models.MarkdownxField(),
        ),
    ]
