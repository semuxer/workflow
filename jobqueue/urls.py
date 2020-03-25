from django.views.generic import RedirectView
from django.conf.urls import handler404, handler500
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^jobs/list/$', views.jobs_list, name='jobs_list'),
    url(r'^jobs/list/sort/$', views.jobs_list_sort, name='jobs_list_sort'),
    url(r'^jobs/addedit/$', views.jobs_addedit, name='jobs_addedit'),
    url(r'^jobs/del/$', views.jobs_del, name='jobs_del'),
    url(r'^jobs/taglink/$', views.taglink, name='taglink'),
    url(r'^jobs/colorset/$', views.jobs_color_set, name='jobs_color_set'),
    url(r'^jobs/tags/aply/$', views.job_tag2newtag, name='job_tag2newtag'),
    url(r'^config/tags/list/$', views.tags_list, name='tags_list'),
    url(r'^config/tags/list/sort/$', views.tags_list_sort, name='tags_list_sort'),
    url(r'^config/tags/addedit/$', views.tags_addedit, name='tags_addedit'),
    url(r'^config/tags/del/$', views.tags_del, name='tags_del'),
    url(r'^config/colors/list/$', views.colors_list, name='colors_list'),
    url(r'^config/colors/list/sort/$', views.colors_list_sort, name='colors_list_sort'),
    url(r'^config/colors/addedit/$', views.colors_addedit, name='colors_addedit'),
    url(r'^config/colors/del/$', views.colors_del, name='colors_del'),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^accounts/loginview/$', views.login_view, name='login_view'),
    url(r'^accounts/logout/$', views.logout_view, name='logout_view'),
    url(r'^accounts/profileview/$', views.profile_view, name='profile_view'),
    url(r'^accounts/userlist/$', views.user_list, name='user_list'),
    url(r'^accounts/useradddelright/$', views.user_adddel_right, name='user_adddel_right'),
    url(r'^accounts/usercreate/$', views.user_create, name='user_create'),
    url(r'^accounts/useredit/$', views.user_edit, name='user_edit'),
    url(r'^accounts/userresetpassword/$', views.user_reset_password, name='user_reset_password'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico'), name='favicon'),

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
