from django.urls import path

from .views import (
    GetCategory,
    CreateCategories,
)

app_name = 'main'
urlpatterns = [
    path('<int:pk>/', GetCategory.as_view(), name='get_category'),
    path('', CreateCategories.as_view(), name='create_categories'),
]
