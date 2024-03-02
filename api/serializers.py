from rest_framework import serializers as rest_serialize

from group.models import Group
from lesson.models import Lesson
from product.models import Product


class LessonSerializer(rest_serialize.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ('name', 'videoUrl')


class ProductSerializer(rest_serialize.ModelSerializer):

    lessons = rest_serialize.SerializerMethodField()
    author = rest_serialize.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'start', 'price', 'lessons', 'author')

    def get_lessons(self, obj):
        return len(Lesson.objects.filter(
                product=Product.objects.get(id=obj.id)))

    def get_author(self, obj):
        return obj.author.username


class GroupSerializer(rest_serialize.ModelSerializer):

    product_name = rest_serialize.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('id', 'name', 'product_name', 'usersInGroup')

    def get_product_name(self, obj):
        return obj.product.name


class ProductListSerializer(rest_serialize.ModelSerializer):

    lesson_count = rest_serialize.SerializerMethodField()
    student_count = rest_serialize.SerializerMethodField()
    buyer_percentage = rest_serialize.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'start', 'price', 'minValue', 'maxValue',
                  'lesson_count', 'student_count', 'buyer_percentage')

    def get_lesson_count(self, obj):
        return obj.lesson_set.count()

    def get_student_count(self, obj):
        return obj.total_users_in_product

    def get_buyer_percentage(self, obj):
        total_users = self.context.get('total_users')
        if total_users == 0:
            return 0
        return round((obj.total_users_in_product / total_users) * 100)
