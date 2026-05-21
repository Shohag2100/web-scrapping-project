import requests
from bs4 import BeautifulSoup
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ScrapeResult
from .serializers import ScrapeRequestSerializer, ScrapeResultSerializer


class ScrapeWebsiteView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request):
		serializer = ScrapeRequestSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		url = serializer.validated_data["url"]

		try:
			response = requests.get(url, timeout=10)
			response.raise_for_status()
		except requests.RequestException as exc:
			return Response(
				{"detail": f"Failed to fetch website: {exc}"},
				status=status.HTTP_400_BAD_REQUEST,
			)

		soup = BeautifulSoup(response.text, "html.parser")
		title = soup.title.string.strip() if soup.title and soup.title.string else ""
		meta_tag = soup.find("meta", attrs={"name": "description"})
		meta_description = meta_tag.get("content", "").strip() if meta_tag else ""
		h1_tags = [tag.get_text(strip=True) for tag in soup.find_all("h1") if tag.get_text(strip=True)]
		links_count = len(soup.find_all("a"))
		text_length = len(soup.get_text(separator=" ", strip=True))

		result = ScrapeResult.objects.create(
			user=request.user,
			url=url,
			title=title,
			meta_description=meta_description,
			h1_tags=h1_tags,
			links_count=links_count,
			text_length=text_length,
		)
		output = ScrapeResultSerializer(result)
		return Response(output.data, status=status.HTTP_201_CREATED)


class ScrapeHistoryView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request):
		queryset = ScrapeResult.objects.filter(user=request.user)
		serializer = ScrapeResultSerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
