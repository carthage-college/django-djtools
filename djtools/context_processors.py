from django.conf import settings


def sitevars(request):
    context = {}
    try:
        context['static_root'] = settings.MEDIA_ROOT
        context['media_root'] = settings.MEDIA_ROOT
        context['media_url'] = settings.MEDIA_URL
        context['static_url'] = settings.STATIC_URL
        context['server_url'] = settings.SERVER_URL
        context['root_url'] = settings.ROOT_URL
        context['login_url'] = settings.LOGIN_URL
        context['logout_url'] = settings.LOGOUT_URL
        context['templates_debug'] = settings.TEMPLATES[0]['OPTIONS']['debug']
        context['debug'] = settings.DEBUG
        # UI helpers for email
        context['dl_dt'] = '''
            style="background:#5f9be3; color:#fff; float:left; font-weight:bold; margin-right:10px; padding:5px; width:200px;"
        '''
        context['dl_dd'] = '''
            style="margin:2px 0; padding:5px 0;"
        '''
        context['dl_detail'] = '''
            style="margin-bottom:5px;"
        '''
        context['dd_desc'] = '''
            style="margin-bottom:7px 0;"
        '''
        context['clear'] = '''
            style="clear:both;"
        '''
    except:
        pass
    return context
