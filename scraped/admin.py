from django.contrib import admin

from .models import ScrapeResult


@admin.register(ScrapeResult)
class ScrapeResultAdmin(admin.ModelAdmin):
	list_display = ("id", "user", "url", "title", "links_count", "created_at")
	search_fields = ("user__email", "url", "title")
	list_filter = ("created_at",)
