from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Recipe
from . import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RecipeDetailSerializer  # noqa this is changed from RecipeSerializer to DetailSerializer, because the get_serializer Detail class
    # more functions will use detail serializer than list serializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):    # this is for the detail view
        """return the serializer class for request"""
        if self.action == 'list':
            return serializers.RecipeSerializer    # noqa we don't use RecipeSerializer() cus we return class instead of instance
        return self.serializer_class

    def perform_create(self, serializer):
        """Create new recipe"""
        serializer.save(user=self.request.user)
