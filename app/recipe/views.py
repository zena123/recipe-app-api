from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient
from .serializers import TagSerializer, IngredientSerializer


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """ manage tags in DB"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_queryset(self):
        """return objects for current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('name')

    def perform_create(self, serializer):
        """assign created tag to current user with perform create"""
        serializer.save(user=self.request.user)


class IngredientViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    """ manage ingredients in DB"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        """return objects for current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('name')

    def perform_create(self, serializer):
        """assign created ingredient to current user"""
        serializer.save(user=self.request.user)
