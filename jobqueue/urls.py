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
    url(r'^config/tags/list/$', views.tags_list, name='tags_list'),
    url(r'^config/tags/list/sort/$', views.tags_list_sort, name='tags_list_sort'),
    url(r'^config/tags/addedit/$', views.tags_addedit, name='tags_addedit'),
    url(r'^config/tags/del/$', views.tags_del, name='tags_del'),
    ]


# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns
    
#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#handler404 = views.error_404
#handler500 = views.error_500
