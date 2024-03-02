from rest_framework import permissions
from django.shortcuts import get_object_or_404
from group.models import Group
from product.models import Product

class InGroupOrAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        product = get_object_or_404(Product, name=view.kwargs.get('name'))

        if product.author == request.user:
            return True

        return Group.objects.filter(product=product, users=request.user).exists()
