from django.urls import path
from .views import SummarizeView, RewriteView

urlpatterns = [
    path('summarize/', SummarizeView.as_view(), name='summarize'),
    path('rewrite/', RewriteView.as_view(), name='rewrite'),
]
