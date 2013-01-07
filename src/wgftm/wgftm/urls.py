from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wgftm.views.home', name='home'),
    # url(r'^wgftm/', include('wgftm.foo.urls')),
    
    # Tournament Manager URLs
    url(r'^login/$', 'TournamentManager.views.tm_login'),
    url(r'^logout/$', 'TournamentManager.views.tm_logout'),
    url(r'^register/$', 'TournamentManager.views.register'),
    url(r'^postregister/$', 'TournamentManager.views.postregister'),
    url(r'^viewuser/$', 'TournamentManager.views.viewuser'),
    url(r'^postlogout/$', 'TournamentManager.views.postlogout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
