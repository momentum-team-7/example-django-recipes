from api.serializers import RecipeSerializer
from recipes.models import Recipe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


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
