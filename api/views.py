from api.serializers import RecipeSerializer
from recipes.models import Recipe
from rest_framework.views import APIView
from rest_framework.response import Response


class RecipeListView(APIView):
    def get(self, request, format=None):
        """
        List all recipes
        """
        # change this to use custom method `for_user()` to restrict query results
        recipes = Recipe.objects.for_user(request.user)
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Create a new recipe
        """
        serializer = RecipeSerializer(data=request.data)

        if serializer.is_valid():
            # save instance
            serializer.save(user=request.user)

            return Response(serializer.data)

        return Response(serializer.errors)
