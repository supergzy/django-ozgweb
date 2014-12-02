#coding:utf-8

import commons
import cfg

def index(request):
	
	res_data = {
		"title": cfg.web_name
	}

	return commons.render_template(request, "admin/index.html", res_data);

def admin(request):
	
	res_data = {
		"title": cfg.web_name
	}

	return commons.render_template(request, "admin/admin.html", res_data);
