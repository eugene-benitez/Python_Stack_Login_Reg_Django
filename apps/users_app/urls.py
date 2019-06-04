from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^addJob$', views.add),
    url(r'^add_job$', views.add_job),
    url(r'^view/(?P<my_val>\d+)$', views.job_info),
    url(r'^edit/(?P<my_val>\d+)$', views.edit_info),
    url(r'^edit_job$', views.edit_job),
    url(r'^delete/(?P<my_val>\d+)$',  views.delete),
    url(r'^addList/(?P<my_val>\d+)$', views.job_list),
]
