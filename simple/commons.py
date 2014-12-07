#coding:utf-8

import os
import sys
import json
import cfg
from django.shortcuts import render
from django.http import JsonResponse
from models import DataClass
from models import Data

#递归删除分类
def dataclass_del(id):
	dc_list = DataClass.objects.filter(parent_id = id)
	
	for dc in dc_list:
		child_count = DataClass.objects.filter(parent_id = dc.id).count()
		if child_count > 0:
			dataclass_del(dc.id)
		
		#删除该分类下面的对应数据
		Data.objects.filter(dataclass_id = dc.id).delete()
		dc.delete()

#递归获取父分类的dict
def dataclass_get(id):
	dataclass = DataClass.objects.get(id = id)
	dataclass_json = json.loads(dataclass.toJSON())
	
	if dataclass_json["parent_id"] != 0:
		dataclass_json["parent"] = dataclass_get(dataclass_json["parent_id"])
	
	return dataclass_json

#递归获取该分类下的分类(返回list)
def dataclass_list(id):
	dc_list = DataClass.objects.filter(parent_id = id).order_by("-sort", "-id")
	dc_list_json = []
	for dc in dc_list:
		item = json.loads(dc.toJSON())
				
		child_count = DataClass.objects.filter(parent_id = item["id"]).count()
		if child_count > 0:
			item["children"] = dataclass_list(item["id"])
			
		dc_list_json.append(item)

	return dc_list_json
	
#公用的render函数，主要加入一些公用变量
def render_template(request, templates, res_data = None):

	response_data = {
		"cfg_jquery": cfg.jquery
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
		return (count / page_size) + 1;
