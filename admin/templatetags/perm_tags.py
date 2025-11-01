from django import template
from admin.permission import user_has, user_has_any

register = template.Library()


@register.simple_tag(takes_context=True)
def has_perm(context, module=None, action="view"):
    request = context['request']
    if action == "any":
        return user_has_any(request.user, module=module)
    return user_has(request.user, module=module, action=action)
