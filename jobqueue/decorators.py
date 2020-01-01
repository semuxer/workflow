from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import Profile, User, Tagtype

def user_admin(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_staff:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'У Вас нет прав администратора.', extra_tags='danger')
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_color(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        rights = user.profile.rights.names()
        if "color" in rights:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'У Вас нет прав изменять цвета задач.', extra_tags='danger')
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_task(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        rights = user.profile.rights.names()
        if "task" in rights:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'У Вас нет прав создавать, изменять и удалять задачам.', extra_tags='danger')
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_tags(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        rights = user.profile.rights.names()
        tid = request.GET.get('tid')
        tn = "tag_%s" % (tid)
        try:
            tt = Tagtype.objects.get(id=tid)
        except:
            tt = "неизвестный тег"
        if tn in rights:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'У Вас нет прав изменять тег "%s".' % (str(tt)), extra_tags='danger')
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
