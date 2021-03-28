from recipes.models import Recipe, Ingredient
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('pk', 'recipe', 'amount', 'item')


class RecipeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    tags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='tag')
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = (
            'pk',
            'user',
            'title',
            'prep_time_in_minutes',
            'cook_time_in_minutes',
            'tags',
            'public',
            'ingredients'
        )
