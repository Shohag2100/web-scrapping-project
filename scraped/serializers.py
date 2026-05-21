from rest_framework import serializers
from django.core.validators import URLValidator

from .models import ScrapeResult


class ScrapeRequestSerializer(serializers.Serializer):
	url = serializers.URLField(validators=[URLValidator(schemes=["http", "https"])])


class ScrapeResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapeResult
        fields = [
            "id",
            "url",
            "title",
            "meta_description",
            "h1_tags",
            "links_count",
            "text_length",
            "created_at",
        ]
