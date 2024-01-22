from django.urls import path
from .views import (
    GetLangsView,
    WikiSearchView,
    WikiSummaryView,
    WikiPageView,
    ArxivSearchView,
    SpringerSearchView,
    LibgenSearchView,
    ImprovementView,
    SentenceCompletionView,
    ArticleListCreateView,
    ArticleRetrieveUpdateDestroyView,
    Aidetection,
    Plagiarismdetection,
    Generatecitation
)

urlpatterns = [
    path("langs", GetLangsView.as_view(), name="get_langs"),
    # wiki
    path("wiki-search", WikiSearchView.as_view(), name="wiki_search"),
    path("wiki-summary", WikiSummaryView.as_view(), name="wiki_summary"),
    path("wiki-page", WikiPageView.as_view(), name="wiki_page"),
    # arxiv-springer-libgen
    path("arxiv-search", ArxivSearchView.as_view(), name="arxiv_search"),
    path("springer-search", SpringerSearchView.as_view(), name="springer_search"),
    path("libgen-search", LibgenSearchView.as_view(), name="libgen_search"),
    # text improvement services
    path("improvement", ImprovementView.as_view(), name="improvement"),
    path("completion", SentenceCompletionView.as_view(), name="completion"),
    # projects or articles
    path("articles", ArticleListCreateView.as_view(), name="articles"),
    path("article/<pk>", ArticleRetrieveUpdateDestroyView.as_view(), name="article"),
    # AI_text_detection
    path("ai-detection", Aidetection.as_view(), name="AI_detection"),
    # Plagiarism detection
    path("plagiarism-detection",  Plagiarismdetection.as_view(), name="Plagiarism_detection")
    # Generate citation
    path("generate-citation",  Generatecitation.as_view(), name="Generate_citation")
   
]
