from django.urls import path

from .views import ScrapeWebsiteView, ScrapeHistoryView

urlpatterns = [
    path("run/", ScrapeWebsiteView.as_view(), name="scrape-run"),
    path("history/", ScrapeHistoryView.as_view(), name="scrape-history"),
]
