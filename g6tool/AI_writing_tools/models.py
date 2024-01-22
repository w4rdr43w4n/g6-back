from django.db import models
from django.contrib.auth import get_user_model
import uuid


class ArticlesModel(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="articles"
    )
    lang = models.CharField(max_length=2, null=True)
    title = models.CharField(max_length=255)
    article = models.TextField(
        default='[{"type":"paragraph","children":[{"text":"Start write form here... "}]}]'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    used_credits = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title}|{ self.id}[{self.user}]|{self.created_at}"


class WikiRewrittenSectionsModel(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    lang = models.CharField(max_length=2, editable=False)
    page_id = models.CharField(max_length=255, editable=False)
    section_id = models.CharField(max_length=255, editable=False)
    original = models.TextField(editable=False)
    generated = models.TextField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    model = models.CharField(max_length=20, editable=False)

    def __str__(self):
        return (self.page_id + " _ " + self.section_id)[:50]


class ImprovementModel(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    text = models.TextField()
    improved_text = models.TextField()


class CompletionModel(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    feed = models.TextField()
    completion = models.TextField(null=True)
    title = models.CharField(max_length=255)
    sentence = models.BooleanField(null=True)


class LiteratureEmbeddingsModel(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    title = models.TextField()
    embeddings = models.TextField()
    paragraphs = models.TextField()
