#coding:utf-8

import os
import sys
from django.shortcuts import render
import cfg

#公用的render函数，主要加入一些公用变量
def render_template(request, templates, res_data = None):

	response_data = {
		"cfg_jquery": cfg.jquery
	}

	if(res_data != None):
		response_data["res_data"] = res_data

	return render(request, templates, response_data)
