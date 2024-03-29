# Generated by Django 4.2.3 on 2024-01-01 23:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticlesModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('lang', models.CharField(max_length=2, null=True)),
                ('title', models.CharField(max_length=255)),
                ('article', models.TextField(default='[{"type":"paragraph","children":[{"text":"Start write form here... "}]}]')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('used_credits', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CompletionModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('feed', models.TextField()),
                ('completion', models.TextField(null=True)),
                ('title', models.CharField(max_length=255)),
                ('sentence', models.BooleanField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImprovementModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('text', models.TextField()),
                ('improved_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LiteratureEmbeddingsModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.TextField()),
                ('embeddings', models.TextField()),
                ('paragraphs', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='WikiRewrittenSectionsModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('lang', models.CharField(editable=False, max_length=2)),
                ('page_id', models.CharField(editable=False, max_length=255)),
                ('section_id', models.CharField(editable=False, max_length=255)),
                ('original', models.TextField(editable=False)),
                ('generated', models.TextField(editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('model', models.CharField(editable=False, max_length=20)),
            ],
        ),
    ]
