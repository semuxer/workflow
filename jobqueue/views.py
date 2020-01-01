from io import BytesIO
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count, F, Func, Q, ExpressionWrapper, Max, Min
from .models import *
from .forms import *
from .decorators import *
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import Http404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, get_user_model
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

################################################################### user
def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user.profile.status:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,"Ошибка при входе. Доступ в систему для данного пользователя закрыт.", extra_tags='danger')
            return redirect('login')
    else:
        messages.error(request,"Ошибка при входе. Проверьте правильность введеных логина и пароля.", extra_tags='danger')
        return redirect('login')

@login_required
def profile_view(request):
    tts = Tagtype.objects.all()
    return render(request, 'profile_detail.html', {"tts":tts,})

@login_required
@user_admin
def user_list(request):
    user = get_user_model()
    users = user.objects.all()
    tts = Tagtype.objects.all()
    return render(request, 'user_list.html', {'users':users, "tts":tts})

@login_required
@user_admin
def user_adddel_right(request):
    uid = request.GET.get("uid")
    tag = request.GET.get("tid")
    rg = request.GET.get("rg")
    user = get_object_or_404(get_user_model(), id=uid)
    rights = user.profile.rights.names()
    if tag:
        tt = get_object_or_404(Tagtype, id=tag)
        tn = "tag_%s" % (tag)
        print(tn)
        if tn in rights:
            user.profile.rights.remove(tn)
        else:
            user.profile.rights.add(tn)
    if (rg == "color") or (rg == "task"):
        if rg in rights:
            user.profile.rights.remove(rg)
        else:
            user.profile.rights.add(rg)
    if rg == 'admin':
        if request.user == user:
            messages.error(request, 'Запрещено изменять права администратора для текущего пользователя!', extra_tags='danger')
        elif user.is_superuser:
            messages.error(request, 'Запрещено изменять права администратора для superuser!', extra_tags='danger')
        else:
            user.is_staff = not user.is_staff
            user.save()
    if rg == 'status':
        if request.user == user:
            messages.error(request, 'Запрощено изменять права доступа для текущего пользователя!', extra_tags='danger')
        elif user.is_superuser:
            messages.error(request, 'Запрещено изменять права доступа для superuser!', extra_tags='danger')
        else:
            user.profile.status = not user.profile.status
            user.profile.save()

    return redirect('user_list')


@login_required
def user_edit(request):
    uid = request.GET.get("uid")
    if uid != 'self':
        if not request.user.is_staff:
            messages.error(request, 'У Вас нет прав редактировать данные других пользователей.', extra_tags='danger')
            raise PermissionDenied
    if uid == 'self':
        usr = request.user
        profile = usr.profile
    else:
        usr = get_object_or_404(get_user_model(), id=uid)
        profile = usr.profile
    if request.method == 'POST':
        user_form = UserEditForm(request.POST)
        profile_form = ProfileEditForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = usr
            user.first_name=user_form.cleaned_data['first_name']
            user.last_name=user_form.cleaned_data['last_name']
            user.email=user_form.cleaned_data['email']
            for key, value in profile_form.cleaned_data.items():
                user.profile.__dict__[key] = value
            try:
                print(user)
                rs = user.save()
                print('save', rs)
                messages.success(request, 'Данные пользователя %s успешно обновлены!' % (user.profile))
            except e:
                print(e)
                messages.error(request, 'Невозможно сохранить данные.', extra_tags='danger')
            if uid == 'self':
                return redirect('profile_view')
            else:
                return redirect('user_list')
        else:
            print(user_form.errors)
            print(profile_form.errors)
            messages.error(request, 'Пожалуйста, исправте ошибки.', extra_tags='danger')
    else:
        user_form = UserEditForm(instance=usr)
        profile_form = ProfileEditForm(instance=profile)
    return render(request, 'staff_edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'worker':None
    })

@login_required
@user_admin
def user_create(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = User.objects.create_user(username=user_form.cleaned_data['username'], first_name=user_form.cleaned_data['first_name'], last_name=user_form.cleaned_data['last_name'], email=user_form.cleaned_data['email'])
            for key, value in profile_form.cleaned_data.items():
                user.profile.__dict__[key] = value
            user.save()
            messages.success(request, 'Пользователь %s успешно добавлен!' % (user))
            return custom_redirect('user_reset_password', uid=user.id)
        else:
            messages.error(request, 'Пожалуйста, исправте ошибки.', extra_tags='danger')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'staff_edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'worker':None
    })

@login_required
def user_reset_password(request):
    uid = request.GET.get("uid")
    if uid == 'self':
        user = request.user
    else:
        user = get_object_or_404(get_user_model(), id=uid)
        if not request.user.is_staff:
            messages.error(request, 'У Вас нет прав изменять пароли других пользователей.', extra_tags='danger')
            raise PermissionDenied

    if request.method == 'POST':
        password_form = PasswordForm(request.POST)
        if password_form.is_valid():
            user.set_password(password_form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Пароль пользователя %s успешно изменен!' % (user))
            if uid == 'self':
                return redirect('profile_view')
            else:
                return redirect('user_list')
        else:
            messages.error(request, 'Пожалуйста, исправте ошибки.', extra_tags='danger')
    else:
        password_form = PasswordForm()
    return render(request, 'form.html', {'form':password_form,})

###################################################################

def custom_redirect(url_name, *args, **kwargs):
    url = reverse(url_name, args = args)
    params = urllib.parse.urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)

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
        print(slist)
        sortedslist = [int(numeric_string) for numeric_string in slist]
        sortedslist.sort()
        print(sortedslist)
        i = 0
        for sl in slist:
            item = mdl.objects.get(id=sl)
            item.order = sortedslist[i]
            item.save()
            i = i + 1
            #print(job, job.order)
        ret = True
    except:
        messages.error(request, 'Ошибка при сортировке!', extra_tags='danger')
        ret = False
    return ret

@login_required
def home(request):
    return redirect('jobs_list')
    #return render(request, 'home.html', {} )

@login_required
@user_task
def jobs_list_sort(request):
    sortids = request.GET.get('sortids')
    if sortids:
        sortjobs(request, sortids, Jobs)
    return redirect('jobs_list')

@login_required
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
        jobs = jobs.filter(
            reduce(operator.or_, (Q(name__icontains=q) for q in slist)) |
            reduce(operator.or_, (Q(customer__icontains=q) for q in slist))
                ).distinct()
    jobs = mypaginator(request,jobs)
    colors = Colors.objects.all()
    return render(request, 'jobs_list.html', {'jobs':jobs,'tts':tts, 'curtts':curtts, 'colors':colors, })

@login_required
@user_task
def jobs_del(request):
    id = request.GET.get('id')
    job = get_object_or_404(Jobs, id=id)
    job.delete()
    return redirect('jobs_list')

@login_required
@user_task
def jobs_addedit(request):
    id = request.GET.get('id')
    if id:
        job = get_object_or_404(Jobs, id=id)
    else:
        job = Jobs()
    cont = {}
    ls = list(Jobs.objects.exclude(customer__exact='').exclude(customer__isnull=True).order_by('customer').values('customer').distinct())
    cont['customers'] =  ls
    print(cont)
    return uform('JobsForm', job, 'jobs_list', request, cont)

@login_required
@user_color
def jobs_color_set(request):
    jid = request.GET.get('jid')
    job = get_object_or_404(Jobs, id=jid)
    cid = request.GET.get('color')
    if cid == "*":
        job.color = None
        job.save()
        return redirect('jobs_list')

    color = get_object_or_404(Colors, id=cid)
    job.color = color
    job.save()
    return redirect('jobs_list')


#################################################################### tags
@login_required
@user_admin
def tags_list_sort(request):
    sortids = request.GET.get('sortids')
    if sortids:
        sortjobs(request, sortids, Tagtype)
    return redirect('tags_list')


@login_required
def tags_list(request):
    tts = Tagtype.objects.all()
    return render(request, 'tags_list.html', {'tts':tts,} )

@login_required
@user_admin
def tags_addedit(request):
    id = request.GET.get('id')
    if id:
        tt = get_object_or_404(Tagtype, id=id)
    else:
        tt = Tagtype()
    ret = uform('TagtypeForm', tt, 'tags_list', request)
    print("tt.id",tt.id, tt.seton)
    if tt.seton:
        jobs = Jobs.objects.all()
        for job in jobs:
            job.tags.add(str(tt.id))
    return ret

@login_required
@user_admin
def tags_del(request):
    id = request.GET.get('id')
    tt = get_object_or_404(Tagtype, id=id)
    #jobs = Jobs.objects.all()
    #jobs.tags.remove(str(tt.id))
    tt.delete()
    return redirect('tags_list')

################################################ Colors

@login_required
@user_admin
def colors_list_sort(request):
    sortids = request.GET.get('sortids')
    if sortids:
        sortjobs(request, sortids, Colors)
    return redirect('colors_list')

@login_required
def colors_list(request):
    colors = Colors.objects.all()

    ls = list(Jobs.objects.values_list('name', flat=True)[:len(colors)])
    print(ls)
    return render(request, 'colors_list.html', {'colors':colors, 'ls':ls} )

@login_required
@user_admin
def colors_addedit(request):
    id = request.GET.get('id')
    if id:
        color = get_object_or_404(Colors, id=id)
    else:
        color = Colors()
    ret = uform('ColorsForm', color, 'colors_list', request)
    return ret

@login_required
@user_admin
def colors_del(request):
    id = request.GET.get('id')
    color = get_object_or_404(Colors, id=id)
    #jobs = Jobs.objects.all()
    #jobs.tags.remove(str(tt.id))
    color.delete()
    return redirect('colors_list')

################################################
def uform(fname, inst, rurl, request, cont = {}):
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
    cont['form'] = form
    return render(request, 'form.html', cont)

@login_required
@user_tags
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
