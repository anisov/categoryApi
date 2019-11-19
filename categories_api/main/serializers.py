from rest_framework import serializers

from .models import Category


class RecursiveField(serializers.Serializer):
    def to_internal_value(self, data: dict) -> dict:
        serializer = self.parent.parent.__class__(
            data=data, context=self.context
        )
        serializer.is_valid(raise_exception=True)

        return serializer.validated_data


class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, required=False)

    class Meta:
        model = Category
        fields = ('id', 'name', 'children')

    def to_representation(self, instance: Category) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'children': instance.children_nodes,
            'siblings': instance.siblings,
            'parents': instance.parents,
        }

    def _recursive_create_categories(
        self, data: dict, parent: Category = None
    ) -> Category:
        obj, _ = Category.objects.get_or_create(
            name=data['name'], parent=parent
        )
        children: list = data.get('children', list())

        for child in children:
            self._recursive_create_categories(child, obj)

        return obj

    def create(self, validated_data: dict) -> Category:
        return self._recursive_create_categories(validated_data)
