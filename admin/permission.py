from accounts.models import RoleUser, RolePermissions


def get_user_role(user):
    try:
        return RoleUser.objects.select_related('role').get(user=user).role
    except RoleUser.DoesNotExist:
        return None


def get_role_permissions(role):
    rp = RolePermissions.objects.select_related('permission').filter(role=role)
    perm_map = {}
    for r in rp:
        perm = r.permission
        if perm.module:
            perm_map[f"module:{perm.module.lower()}"] = r
        if perm.path:
            perm_map[f"path:{perm.path.lower()}"] = r
    return perm_map


def user_has(user, module=None, path=None, action="view"):
    role = get_user_role(user)
    if not role:
        return False

    action = action.lower().strip()
    perm_map = get_role_permissions(role)

    key = f"module:{module.lower()}" if module else f"path:{path.lower()}"
    r = perm_map.get(key)

    if not r:
        return False

    permissions = {
        "view": r.has_view,
        "create": r.has_create,
        "add": r.has_create,     
        "edit": r.has_edit,
        "update": r.has_edit,    
        "delete": r.has_delete,
        "remove": r.has_delete  
    }

    return permissions.get(action, False)


def user_has_any(user, module=None, path=None):
    role = get_user_role(user)
    if not role:
        return False

    perm_map = get_role_permissions(role)

    key = f"module:{module.lower()}" if module else f"path:{path.lower()}"
    r = perm_map.get(key)

    if not r:
        return False

    return r.has_view or r.has_create or r.has_edit or r.has_delete
