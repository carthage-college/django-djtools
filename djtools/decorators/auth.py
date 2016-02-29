from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import user_passes_test


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
