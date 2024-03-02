from django.db.models import Count
from group.models import Group


def add_user_to_groups(product, user):

    groups = Group.objects.filter(product=product).annotate(num_users=Count('usersInGroup'))
    match_groups = groups.filter(num_users__lt=product.maxValue).order_by('num_users')

    if match_groups.exists():
        for group in match_groups:
            group.usersInGroup.add(user)
            return group
    else:
        new_group = Group.objects.create(name=product.name, product=product)
        new_group.usersInGroup.add(user)
        return rebuild_groups(groups)
    
    return None
    
def rebuild_groups(groups):

    groups = groups.order_by('num_users')
    
    while groups.last().num_users - groups.first().num_users > 1:
        min_group = groups.first()
        max_group = groups.last()

        user_to_move = max_group.usersInGroup.first()
        max_group.usersInGroup.remove(user_to_move)
        min_group.usersInGroup.add(user_to_move)

        groups = groups.order_by('num_users')

    return groups
