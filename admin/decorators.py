from functools import wraps
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .permission import user_has, user_has_any


def superuser_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect("/admin/unauthorized/")
        return view_func(request, *args, **kwargs)
    return wrapper


def permission_required(module=None, action="view", path=None, redirect_to_login=True):
    """
    Usage Examples:
      @permission_required(module="products", action="any")
      @permission_required(module="products", action="view")
      @permission_required(path="/admin/orders/", action="any")
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):

            if not request.user.is_authenticated:
                if redirect_to_login:
                    return HttpResponseRedirect(reverse('admin_login'))
                return render(request, "admin/unauthorized.html", status=403)

            # superuser gets full access
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Check for ANY permission for module
            if action == "any":
                allowed = user_has_any(request.user, module=module, path=path)
            else:
                allowed = user_has(request.user, module=module, path=path, action=action)

            if not allowed:
                return render(request, "admin/unauthorized.html", status=403, context={
                    "module": module,
                    "action": action
                })

            return view_func(request, *args, **kwargs)

        return _wrapped
    return decorator
