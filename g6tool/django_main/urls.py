from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import GetApiEndPointsView

# from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html")),
    path("admin/", admin.site.urls),
    path("api/v1", GetApiEndPointsView.as_view()),
    path("api/v1/tools/", include("AI_writing_tools.urls")),
    path("api/v1/auth/", include("accounts.urls")),
    # path("auth/", include("allauth.urls")),
]
