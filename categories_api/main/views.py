from rest_framework import generics
from rest_framework import status
from rest_framework.views import Response

from .serializers import CategorySerializer
from .models import Category


class BaseCategoryApi:
    queryset = Category.objects.all()


class CreateCategories(BaseCategoryApi, generics.CreateAPIView):
    serializer_class = CategorySerializer

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response(status=status.HTTP_201_CREATED)


class GetCategory(BaseCategoryApi, generics.RetrieveAPIView):
    serializer_class = CategorySerializer
