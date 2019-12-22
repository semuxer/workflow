from io import BytesIO
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count, F, Func, Q, ExpressionWrapper, Max, Min
from .models import Jobs, Tagtype
from .forms import *
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import Http404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
import datetime, time
import pytz
import math
import json
import collections
from xlutils.copy import copy
from copy import deepcopy
import hashlib
import binascii
import urllib
import operator
import re
import calendar
from monthdelta import monthdelta
from django.db.models.fields import DurationField
from django.template.loader import render_to_string, get_template
import sys
import os
from functools import reduce

def str2list(st):
    def  allfunc(sa):
        out = []
        out.append(sa)
        out.append(sa.capitalize())
        out.append(sa.lower())
        out.append(sa.upper())
        out.append(sa.title())
        return out

    st = st.strip()
    lst = []
    lst = lst + allfunc(st)
    st = re.sub(' +', ' ', st)
    lst = lst + allfunc(st)

    tmpls = st.split(" ")
    for tmpl in tmpls:
        lst = lst + allfunc(tmpl)

    return lst

def store(request, val, df = None):
    nv = request.GET.get(val)
    if not nv:
        ov = request.session.get(val)
        if not ov:
            request.session[val] = df
            return df
        else:    
            return ov
    else:
        request.session[val] = nv
        return nv

def mypaginator(request, plts, limit=100):
    paginator = Paginator(plts, limit)
    page = request.GET.get('page')
    try:
        plts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        plts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        plts = paginator.page(paginator.num_pages)        
    return plts

def sortjobs(request, sortids, mdl):
    try:
        slist = sortids.split(',')
        sortedslist = slist.copy()
        sortedslist.sort()
        #print(sortedslist)
        i = 0
        for sl in slist:
            item = mdl.objects.get(id=sl)
            item.order = sortedslist[i]
            item.save()
            i = i + 1
            #print(job, job.order)
        ret = True
    except:
        messages.error(request, 'Помилка при сортуванні!', extra_tags='danger')
        ret = False
    return ret

def home(request):
    return redirect('jobs_list')

def jobs_list_sort(request):
    sortids = request.GET.get('sortids')
    if sortids:
        sortjobs(request, sortids, Jobs)
    return redirect('jobs_list')

def jobs_list(request):
    action = request.GET.get('action')
    print("action",action)
    search = None
    if action == "get":
        search = store(request,'search')
    elif action == "rst":
        request.session['search'] = None

    print('search',search)
    cur_tag = store(request,'cur_tag')
    try:
        curtts = Tagtype.objects.get(id=cur_tag)
    except:
        curtts = None
    flt = store(request,'flt', 0)
    print(curtts,flt)
    jobs = Jobs.objects.all()
    tts = Tagtype.objects.all()
    if curtts:
        if flt == "0":
            jobs = jobs.exclude(tags__name__in=[cur_tag])
        elif flt == "1":
            jobs = jobs.filter(tags__name__in=[cur_tag])
    if search:
        slist = str2list(search)
        jobs = jobs.filter(reduce(operator.or_, (Q(name__icontains=q) for q in slist))).distinct()

    jobs = mypaginator(request,jobs)

    return render(request, 'jobs_list.html', {'jobs':jobs,'tts':tts, 'curtts':curtts,})

def jobs_del(request):
    id = request.GET.get('id')
    job = get_object_or_404(Jobs, id=id)
    job.delete()
    return redirect('jobs_list')

def jobs_addedit(request):
    id = request.GET.get('id')
    if id:
        job = get_object_or_404(Jobs, id=id)
    else:
        job = Jobs()
    return uform('JobsForm', job, 'jobs_list', request)

def tags_list_sort(request):
    sortids = request.GET.get('sortids')
    if sortids:
        sortjobs(request, sortids, Tagtype)
    return redirect('tags_list')

def tags_list(request):
    tts = Tagtype.objects.all()
    return render(request, 'tags_list.html', {'tts':tts,} )

def tags_addedit(request):
    id = request.GET.get('id')
    if id:
        tt = get_object_or_404(Tagtype, id=id)
    else:
        tt = Tagtype()
    return uform('TagtypeForm', tt, 'tags_list', request)

def tags_del(request):
    id = request.GET.get('id')
    tt = get_object_or_404(Tagtype, id=id)
    tt.delete()
    return redirect('tags_list')

def uform(fname, inst, rurl, request):
    id = request.GET.get('id')
    if request.method == 'POST':
        form = globals()[fname](request.POST, instance=inst)
        if form.is_valid():
            form.save()
            if id:
                messages.success(request, 'Данные записи "%s" были успешно изменены!' % (inst))
            else:
                messages.success(request, 'Данные записи "%s" были успешно добавлены!' % (inst))
            return redirect(rurl)
        else:
            messages.error(request, 'Будь ласка, виправте помилки.', extra_tags='danger')
    else:
        form = globals()[fname](instance=inst)
    print("!!!!!",form.form_title)
    return render(request, 'form.html', { 'form': form })

def taglink(request):
    jid = request.GET.get('jid')
    job = get_object_or_404(Jobs, id=jid)
    tid = request.GET.get('tid')
    tt = get_object_or_404(Tagtype, id=tid)
    ctags = job.tags.names()
    if tid in ctags:
        job.tags.remove(str(tt.id))
    else:
        job.tags.add(str(tt.id))
    return redirect('jobs_list')

