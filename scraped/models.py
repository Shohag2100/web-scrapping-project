from django.conf import settings
from django.db import models


class ScrapeResult(models.Model):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="scrape_results",
	)
	url = models.URLField()
	title = models.CharField(max_length=500, blank=True)
	meta_description = models.TextField(blank=True)
	h1_tags = models.JSONField(default=list, blank=True)
	links_count = models.PositiveIntegerField(default=0)
	text_length = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"{self.user} - {self.url}"
