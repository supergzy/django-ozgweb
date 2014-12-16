
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	
	#后台页面部分
	url(r'^admin/index$', 'simple.views_admin.index'),
	url(r'^admin/admin$', 'simple.views_admin.admin'),
	
	#验证码
	url(r'^admin/get_code$', 'simple.views_admin.get_code'),

	#后台请求数据部分
	url(r'^admin/ajax_login$', 'simple.views_admin.ajax_login'),
	url(r'^admin/ajax_logout$', 'simple.views_admin.ajax_logout'),
	url(r'^admin/ajax_menu_list$', 'simple.views_admin.ajax_menu_list'),
	url(r'^admin/ajax_admin_list$', 'simple.views_admin.ajax_admin_list'),
	url(r'^admin/ajax_admin_add$', 'simple.views_admin.ajax_admin_add'),
	url(r'^admin/ajax_admin_del$', 'simple.views_admin.ajax_admin_del'),
	url(r'^admin/ajax_admin_updatepwd$', 'simple.views_admin.ajax_admin_updatepwd'),	
	url(r'^admin/ajax_art_single_get$', 'simple.views_admin.ajax_art_single_get'),
	url(r'^admin/ajax_art_single_update$', 'simple.views_admin.ajax_art_single_update'),	
	url(r'^admin/ajax_dataclass_list$', 'simple.views_admin.ajax_dataclass_list'),
	url(r'^admin/ajax_dataclass_get$', 'simple.views_admin.ajax_dataclass_get'),	
	url(r'^admin/ajax_dataclass_add$', 'simple.views_admin.ajax_dataclass_add'),
	url(r'^admin/ajax_dataclass_del$', 'simple.views_admin.ajax_dataclass_del'),	
	url(r'^admin/ajax_data_list$', 'simple.views_admin.ajax_data_list'),
	url(r'^admin/ajax_data_get$', 'simple.views_admin.ajax_data_get'),	
	url(r'^admin/ajax_data_add$', 'simple.views_admin.ajax_data_add'),
	url(r'^admin/ajax_data_del$', 'simple.views_admin.ajax_data_del'),
	
	#前台
	url(r'^site/index$', 'simple.views_site.index'),

)
