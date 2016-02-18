from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import available_attrs
from django.http import HttpResponseRedirect
from django.utils.encoding import force_str
#from django.utils.functional import wraps
from django.shortcuts import resolve_url
from django.contrib.auth import login

from djzbar.utils.mssql import get_userid
from djtools.utils.users import in_group

from functools import wraps

def portal_auth_required(session_var, group=None, redirect_url=None):
    def _portal_auth_required(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def wrapper(request, *args, **kwargs):
            resolved_redirect_url = force_str(
                resolve_url(redirect_url or reverse_lazy("auth_login"))
            )
            if not request.session.get(session_var):
                if not request.user.is_authenticated():
                    # coming from the portal with uid set?
                    uid = request.GET.get('uid')
                    if uid:
                        # do we have a user id or portal id?
                        if len(uid) > 12:
                            uid = get_userid(request.GET.get('uid'))
                        try:
                            user = User.objects.get(pk=uid.strip("0"))
                        except:
                            # nope
                            return HttpResponseRedirect(reverse_lazy("auth_login"))
                    else:
                        return HttpResponseRedirect(reverse_lazy("auth_login"))
                else:
                    user = request.user
                if group:
                    if not in_group(user, group) and not user.is_superuser:
                        return HttpResponseRedirect(resolved_redirect_url)
                # sign in the user manually
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                request.session[session_var] = True

            return view_func(request, *args, **kwargs)
        return wrapper
    return _portal_auth_required


def superuser_only(function):
    """
    Limit view to superusers only.
    Usage:
    --------------------------------------------------------------------------
    @superuser_only
    def my_view(request):
        ...
    --------------------------------------------------------------------------
    or in urls:
    --------------------------------------------------------------------------
    urlpatterns = patterns('',
        (r'^foobar/(.*)', superuser_only(my_view)),
    )
    --------------------------------------------------------------------------
    """
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            #raise PermissionDenied
            return HttpResponseRedirect(reverse_lazy("auth_login"))
        return function(request, *args, **kwargs)
    return _inner


def group_required(*group_names):
    """
    Requires user membership in at least one of the groups passed in:

    @group_required('admins','editors')
    def myview(request, id):

    """
    def in_groups(u):
        if u.is_authenticated():
            if u.is_superuser or bool(u.groups.filter(name__in=group_names)):
                return True
        return False
    return user_passes_test(in_groups)
