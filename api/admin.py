from django.contrib import admin
from group.models import Group
from lesson.models import Lesson
from product.models import Product


admin.site.register(Product)
admin.site.register(Lesson)
admin.site.register(Group)
