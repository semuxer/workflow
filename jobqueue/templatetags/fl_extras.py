import re
from django import template
from django.urls import reverse
from django.utils import timezone
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import math
from xml.sax import saxutils as su
from jobqueue.models import Tagtype

register = template.Library()

#my filter
@register.filter
def checktag(job, tt):
    th = job.checknt(tt.id)
    return th

@register.filter
def faicon(v, color):
    rgb = {"text-success":"rgb(40, 167, 69)", "text-black-50":"rgba(0,0,0,.5)", "text-light":"rgb(248, 249, 250)" }
    if v.icon3:
        try:
            txt = '<span data-toggle="tooltip" data-placement="top"><style>svg {width: 1em; height: 1em;}</style>%s</span>' % (v.icon3)
            txt = re.sub(r'fill="#(?!fff).*?"', 'fill="%s"' % rgb.get(color), txt)
            txt = re.sub(r'<title>.*?<\/title>', '<title>%s</title>' % v.name, txt)
        except:
            txt = ""
    else:
        try:
            txt = '<i class="%s %s" data-toggle="tooltip" data-placement="top" title="%s"></i>' % (v.icon2, color, v.name)
        except:
            txt = ""
    return mark_safe(txt)

@register.filter
def parsetags(v):
    #print(v.html_name)
    txt = su.unescape(str(v))
    return mark_safe(txt)

@register.filter
def is_current_page(request, param):
    params = param.split(',')
    name = params[0]
    return request.path == reverse(name)

@register.filter
def addcss(v, param):
    regex = r"class=\"(.*?)\""
    print(v, param)
    match = re.search(regex, str(v))
    if match:
        v = str(v).replace(match[0], "%s %s" % (match[0],param))
    else:
        v = str(v).replace(">", ' class="%s">' % (param))
    return mark_safe(v)

@register.filter
def index(v, param):
    #print(v, param)
    #print(v.index(param))
    try:
        out = v[param]
    except:
        out = ""
    return out

@register.filter
def chekrights(v,param):
    #print('param',param)
    # try:
    #     tg = Tagtype.objects.filter(name=param)[0]
    #     techop = tg.techop
    # except:
    #     techop = False
    #print('techop',techop)
    try:
        tn = "tag_%s" % (param.id)
        if v.profile.checkrights(tn):
            out = True
        else:
            out = False
    except:
        if v.profile.checkrights(param):
            out = True
        else:
            out = False
    #if techop and v.profile.checkrights('task'):
    #if v.profile.checkrights('task'):
    #    out = True
    #print(param, out)
    return out


@register.filter
def yn(v):
    if v == True:
        return "Да"
    elif v == False:
        return "Нет"
    elif v == None:
        return ""
    else:
        return v
