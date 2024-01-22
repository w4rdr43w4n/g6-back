from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from .models import (
    ArticlesModel,
    WikiRewrittenSectionsModel,
    ImprovementModel,
    CompletionModel,
)
from .Utils.ai_utils import Wiki
from accounts.serializers import CustomUserSerializer


class WikiSearchSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=50, default="", trim_whitespace=True)
    n = serializers.IntegerField(max_value=40, default=10, min_value=3)
    lang = serializers.ChoiceField(choices=Wiki.langs, default="en")


class WikiPageSerializer(serializers.Serializer):
    page_id = serializers.CharField(max_length=255)
    # language = serializers.CharField(max_length=2)
    lang = serializers.ChoiceField(choices=Wiki.langs)


class ImprovementSerializer(serializers.ModelSerializer):
    improved_text = serializers.CharField(read_only=True, default="")
    # lang = serializers.ChoiceField(choices=Wiki.langs)

    class Meta:
        model = ImprovementModel
        fields = "__all__"


class ArticlesSerializer(serializers.ModelSerializer):
    lang = serializers.ChoiceField(choices=Wiki.langs)
    used_credits = serializers.IntegerField(read_only=True)
    user_name = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = ArticlesModel
        fields = "id", "lang", "title", "used_credits", "user_name", "created_at", "modified_at"


class ArticlesUpdateSerializer(serializers.ModelSerializer):
    lang = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    user_name = serializers.CharField(source="user.username", read_only=True)
    used_credits = serializers.IntegerField(read_only=True)

    class Meta:
        model = ArticlesModel
        fields = "id", "lang", "title", "article", "used_credits", "user_name", "created_at", "modified_at"


class WikiRewrittenSectionsSerializer(serializers.ModelSerializer):
    lang = serializers.ChoiceField(choices=Wiki.langs)

    class Meta:
        model = WikiRewrittenSectionsModel
        fields = "__all__"


class CompletionSerializer(serializers.ModelSerializer):
    # lang = serializers.ChoiceField(choices=Wiki.langs)

    class Meta:
        model = CompletionModel
        fields = "title", "feed", "sentence"


# ################   start ITI PROJECT   #######################


class MyUserDetailsSerializer(UserDetailsSerializer):
    """
    User model w/o password
    """

    class Meta:
        model = get_user_model()
        extra_fields = []

        extra_fields.append(model.USERNAME_FIELD)
        extra_fields.append(model.EMAIL_FIELD)
        extra_fields.append("first_name")
        extra_fields.append("last_name")
        extra_fields.append("is_staff")
        fields = ("pk", *extra_fields)
        read_only_fields = ("email", "is_staff")
