#coding:utf-8

import commons

def index(request):

	return commons.render_template(request, "site/index.html")
