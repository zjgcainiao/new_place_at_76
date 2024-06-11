from django.contrib.auth.models import Group, Permission


def create_group(name, permissions=None):
    group, created = Group.objects.get_or_create(name=name)
    if permissions:
        # permissions should be a list of permission names
        group_permissions = Permission.objects.filter(codename__in=permissions)
        group.permissions.set(group_permissions)
    group.save()
    return group


# Example usage
create_group('Technical', permissions=[
             'add_repairorder', 'change_repairorder'])
