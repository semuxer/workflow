from django.views.generic import RedirectView
from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, re_path

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^jobs/list/$', views.jobs_list, name='jobs_list'),
    re_path(r'^jobs/list/sort/$', views.jobs_list_sort, name='jobs_list_sort'),
    re_path(r'^jobs/addedit/$', views.jobs_addedit, name='jobs_addedit'),
    re_path(r'^jobs/del/$', views.jobs_del, name='jobs_del'),
    re_path(r'^jobs/taglink/$', views.taglink, name='taglink'),
    re_path(r'^jobs/colorset/$', views.jobs_color_set, name='jobs_color_set'),
    re_path(r'^jobs/tags/aply/$', views.job_tag2newtag, name='job_tag2newtag'),
    re_path(r'^config/tags/list/$', views.tags_list, name='tags_list'),
    re_path(r'^config/tags/list/sort/$', views.tags_list_sort, name='tags_list_sort'),
    re_path(r'^config/tags/addedit/$', views.tags_addedit, name='tags_addedit'),
    re_path(r'^config/tags/del/$', views.tags_del, name='tags_del'),
    re_path(r'^config/colors/list/$', views.colors_list, name='colors_list'),
    re_path(r'^config/colors/list/sort/$', views.colors_list_sort, name='colors_list_sort'),
    re_path(r'^config/colors/addedit/$', views.colors_addedit, name='colors_addedit'),
    re_path(r'^config/colors/del/$', views.colors_del, name='colors_del'),
    re_path(r'^accounts/login/$', auth_views.LoginView.as_view(), name='login'),
    re_path(r'^accounts/loginview/$', views.login_view, name='login_view'),
    re_path(r'^accounts/logout/$', views.logout_view, name='logout_view'),
    re_path(r'^accounts/profileview/$', views.profile_view, name='profile_view'),
    re_path(r'^accounts/userlist/$', views.user_list, name='user_list'),
    re_path(r'^accounts/useradddelright/$', views.user_adddel_right, name='user_adddel_right'),
    re_path(r'^accounts/usercreate/$', views.user_create, name='user_create'),
    re_path(r'^accounts/useredit/$', views.user_edit, name='user_edit'),
    re_path(r'^accounts/userresetpassword/$', views.user_reset_password, name='user_reset_password'),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico'), name='favicon'),

    #url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    #url(r'^accounts/profile/$', views.profile, name='profile'),
    #url(r'^accounts/profileedit/$', views.profile_edit, name='profile_edit'),
    #url(r'^accounts/profilepasschange/$', views.profile_password_change, name='profile_password_change'),
   ]


# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         url('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns

#path('__debug__/', include(debug_toolbar.urls)),

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#handler404 = views.error_404
#handler500 = views.error_500
