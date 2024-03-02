from rest_framework import status, generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Count
from group.models import Group
from lesson.models import Lesson
from product.models import Product
from api.serializers import ProductSerializer, LessonSerializer, ProductListSerializer, GroupSerializer
from api.utils import add_user_to_groups
from django.db.models import Subquery
from .permissions import InGroupOrAuthor


class ProductListView(generics.ListAPIView):

    queryset = Product.objects.prefetch_related('lesson_set', 'group_set').annotate(total_users_in_product=Count('group__usersInGroup')).all()
    serializer_class = ProductListSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['total_users'] = User.objects.count()
        return context


class ProductAccessAPIView(generics.RetrieveAPIView):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'name'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.access(instance, serializer, request.user)

    def access(self, instance, serializer, user):

        if instance.author == user or Group.objects.filter(product=instance, usersInGroup=user).exists():
            return Response(serializer.data, status=status.HTTP_200_OK)

        if add_user_to_groups(instance, user) is None:
            return Response({'message': 'Группы переполнены'}, status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LessonListView(generics.ListAPIView):

    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, InGroupOrAuthor]
    lookup_field = 'name'

    def get_queryset(self):
        name = self.kwargs.get('name')
        product_ids = Product.objects.filter(name=name).values_list('id', flat=True)
        lessons = Lesson.objects.filter(product_id__in=Subquery(product_ids))
        return lessons

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GroupListAPIView(generics.ListAPIView):

    queryset = Group.objects.all().prefetch_related('usersInGroup').select_related('product')
    serializer_class = GroupSerializer
