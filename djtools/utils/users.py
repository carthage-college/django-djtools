from django.contrib.auth.models import User


def in_group(user, *args):
    '''
    Determine whether or not a user belongs to a group or groups.
    If more than one group is passed, then validity is based on
    membership in at least one of the groups in the list. The user
    does not have to belong to all groups in the list.

    Accepts a user object and a list of groups, like so:

    facstaff = in_group(
        request.user,
        "carthageStaffStatus","carthageFacultyStatus"
    )
    '''

    g = False
    if user:
        for arg in args:
            g = user.groups.filter(name=arg).exists()
            if g:
                g = True
                break

    # superuser exception
    if not g and user.is_superuser:
        g = True

    return g


def faculty_staff(cid):
    '''
    is user faculty or staff?
    '''

    try:
        user = User.objects.get(pk=cid)
        status = in_group(user, "carthageStaffStatus","carthageFacultyStatus")
    except:
        status = False
    return status
