def in_group(user, *args):
    g = False
    if user:
        for arg in args:
            g = user.groups.filter(name=arg).exists()
            if g:
                g = True
                break
    return g
