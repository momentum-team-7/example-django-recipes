from api.serializers import RecipeSerializer
from recipes.models import Recipe
from rest_framework.views import APIView
from rest_framework.response import Response


class RecipeListView(APIView):
    def get(self, request, format=None):
        """
        List all recipes
        """
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)
