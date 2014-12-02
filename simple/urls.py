#coding:utf-8

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	
	#后台
	url(r'^admin/index$', 'simple.views_admin.index'),
	url(r'^admin/admin$', 'simple.views_admin.admin'),
	
	#前台
	url(r'^site/index$', 'simple.views_site.index'),

)
