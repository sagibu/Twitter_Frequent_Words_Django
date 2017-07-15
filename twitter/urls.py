from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^printer/(?P<topic>\w+)', views.printer, name='print'),
    url(r'^monitor/(?P<topic>\w+)', views.monitor, name='monitor'),
    url(r'^count/(?P<topic>\w+)', views.count, name='count'),
]
