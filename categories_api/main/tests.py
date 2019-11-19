from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


class TestCategoriesApi(APITestCase):
    url_create_categories = reverse('main:create_categories')
    api_client = APIClient()

    def test_integration_categories_api(self):
        data = {
            "name": "Category 1",
            "children": [
                {
                    "name": "Category 1.1",
                    "children": [
                        {
                            "name": "Category 1.1.1",
                            "children": [
                                {"name": "Category 1.1.1.1"},
                                {"name": "Category 1.1.1.2"},
                                {"name": "Category 1.1.1.3"},
                            ],
                        },
                        {
                            "name": "Category 1.1.2",
                            "children": [
                                {"name": "Category 1.1.2.1"},
                                {"name": "Category 1.1.2.2"},
                                {"name": "Category 1.1.2.3"},
                            ],
                        },
                    ],
                },
                {
                    "name": "Category 1.2",
                    "children": [
                        {"name": "Category 1.2.1"},
                        {
                            "name": "Category 1.2.2",
                            "children": [
                                {"name": "Category 1.2.2.1"},
                                {"name": "Category 1.2.2.2"},
                            ],
                        },
                    ],
                },
            ],
        }
        response = self.api_client.post(
            self.url_create_categories, data=data, format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        response = self.api_client.get(
            reverse('main:get_category', kwargs={'pk': 8})
        )
        assert response.status_code == status.HTTP_200_OK
        data = {
            "id": 8,
            "name": "Category 1.1.2.1",
            "parents": [
                {"id": 7, "name": "Category 1.1.2"},
                {"id": 2, "name": "Category 1.1"},
                {"id": 1, "name": "Category 1"},
            ],
            "children": [],
            "siblings": [
                {"id": 9, "name": "Category 1.1.2.2"},
                {"id": 10, "name": "Category 1.1.2.3"},
            ],
        }
        assert response.data == data
