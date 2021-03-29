from api.serializers import RecipeSerializer, IngredientSerializer
from recipes.models import Recipe, Ingredient
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView


# see the docs here for the methods and attributes you can set
# when you use these Generic Views:
# https://docs.djangoproject.com/en/stable/api-guide/generic-views#genericapiview
class RecipeListCreateView(ListCreateAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        # see models.py for the `for_user` method definition
        return Recipe.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecipeDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return Recipe.objects.for_user(self.request.user)

        return self.request.user.recipes


class IngredientCreateView(CreateAPIView):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

    def perform_create(self, serializer):
        recipe = serializer.validated_data['recipe']
        if self.request.user != recipe.user:
            raise PermissionDenied(
                detail="You are not the owner of this recipe.")
        serializer.save()


class IngredientDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

    def get_queryset(self):
        # Filter down and make sure users can't update or delete
        # ingredients on recipes that don't belong to them
        return Ingredient.objects.filter(recipe__user=self.request.user)
