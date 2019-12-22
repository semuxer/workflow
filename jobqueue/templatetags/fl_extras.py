import re
from django import template
from django.urls import reverse
from django.utils import timezone
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import math
from xml.sax import saxutils as su

register = template.Library()

#my filter
@register.filter
def checktag(job, tt):
    th = job.tags.names()
    if str(tt.id) in th:
        return True
    else:
        return False

@register.filter
def faicon(v, color):
    txt = '<i class="%s %s" data-toggle="tooltip" data-placement="top" title="%s"></i>' % (v.icon2, color, v.name)
    #txt = '<i class="material-icons %s" data-placement="top" title="%s">%s</i>' % (color, v.name, v.icon2)
    #txt = v#'<i class="'+v+'"></i>'
    #print(txt)
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

