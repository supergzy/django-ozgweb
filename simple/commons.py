#coding:utf-8

import os
import sys
import cfg
from django.shortcuts import render
from django.http import JsonResponse

#公用的render函数，主要加入一些公用变量
def render_template(request, templates, res_data = None):

	response_data = {
		"cfg_jquery": cfg.jquery,
		"cfg_title": cfg.web_name
	}

	if(res_data != None):
		response_data["res_data"] = res_data

	return render(request, templates, response_data)

#仅在这个模块用到
def res(res_code, desc, data):
	res_data = {
		"code": res_code,
		"desc": desc,
	}

	if data:
		res_data["data"] = data
	
	response = JsonResponse(res_data)
	return response

#回应请求成功
def res_success(desc, data = None):
	return res(0, desc, data)
#回应请求失败
def res_fail(res_code, desc, data = None):
	return res(res_code, desc, data)

#计算总页数
def page_count(count, page_size):
	if(count % page_size == 0):
		return (count / page_size)
	else:
		return (count / page_size) + 1
