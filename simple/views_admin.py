#coding:utf-8

import commons
import cfg
import json
import time
import sys
import os
import platform
import django
from DjangoCaptcha import Captcha
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from models import Admin
from models import ArtSingle
from models import DataClass
from models import Data

def index(request):
	#如果已登录就直接跳到管理界面
	if request.session.get("sess_admin", False):
		return HttpResponseRedirect("admin")
	
	res_data = {
		"title": cfg.web_name,
	}

	return commons.render_template(request, "admin/index.html", res_data);

def admin(request):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return HttpResponseRedirect("index")
	
	system = platform.uname()
	
	res_data = {
		"title": cfg.web_name,
		"django_version": django.get_version(),
		"python_version": platform.python_version(),
		"system": system[0] + " " + system[2],
	}
	
	return commons.render_template(request, "admin/admin.html", res_data);

def get_code(request):
	ca = Captcha(request)
	#ca.words = ['hello', 'world', 'helloworld']
	ca.type = 'number' #or word
	ca.img_width = 150
	ca.img_height = 30
	return ca.display()

def ajax_login(request):

	imgcode = request.GET.get("code")
	print imgcode
	if not imgcode or imgcode == "":
		return commons.res_fail(1, "验证码不能为空")

	ca = Captcha(request)
	if ca.check(imgcode):
		
		name = request.GET.get("name")
		pwd = request.GET.get("pwd")
		
		try:
			admin = Admin.objects.get(name = name, pwd = pwd)
			admin_jsonstr = admin.toJSON()
			admin = json.loads(admin_jsonstr)
			
			#删除密码字段
			del(admin["pwd"])	
			request.session["sess_admin"] = admin
			
			return commons.res_success("登录成功")
		except:
			return commons.res_fail(1, "用户或密码不正确")
			
	else:
		return commons.res_fail(1, "验证码不正确")

def ajax_logout(request):	
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")
	
	del request.session["sess_admin"]
	return commons.res_success("退出登录")

def ajax_menu_list(request):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")

	return commons.res_success("请求成功", cfg.admin_menu_list)
	
def ajax_admin_list(request):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")
	
	#分页索引和每页显示数
	page = 1
	if request.REQUEST.get("page"):
		page = int(request.REQUEST.get("page"))
	page_size = cfg.page_size
	if request.REQUEST.get("page_size"):
		page_size = int(request.REQUEST.get("page_size"))
	
	total = Admin.objects.all().count()
	page_count = commons.page_count(total, page_size)
	
	offset = (page - 1) * page_size
	limit = offset + page_size
	admin_list = Admin.objects.all().order_by("-id")[offset:limit]
	
	admin_list_json = []
	for admin in admin_list:		
		item = json.loads(admin.toJSON())
		item["add_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item["add_time"]));
		del item["pwd"]
		admin_list_json.append(item)
	
	res_data = {
		"page_size": page_size,
		"page_count": page_count,
		"total": total,
		"page": page,
		"list": admin_list_json,
	}
	
	return commons.res_success("请求成功", res_data)

def ajax_admin_add(request):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")
	
	name = request.REQUEST.get("name")
	pwd = request.REQUEST.get("pwd")
	pwd2 = request.REQUEST.get("pwd2")
	
	if name == "":
		return commons.res_fail(1, "用户名不能为空")
	if pwd == "":
		return commons.res_fail(1, "密码不能为空")
	if pwd != pwd2:
		return commons.res_fail(1, "确认密码不正确")
	
	total = Admin.objects.filter(name = name).count()
	if total > 0:
		return commons.res_fail(1, "该管理员已存在")
	
	admin = Admin(
		name = name,
		pwd = pwd,
		add_time = int(time.time())
	)
	admin.save()
	
	return commons.res_success("添加成功", json.loads(admin.toJSON()))

def ajax_admin_del(request):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")
	
	id = request.REQUEST.get("id")
		
	try:
		admin = Admin.objects.get(id = id)
		admin.delete()
		return commons.res_success("删除成功")
	except:
		return commons.res_fail(1, "该数据不存在")

def ajax_admin_updatepwd(request):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")
	
	curr_admin = request.session.get("sess_admin")
	old_pwd = request.REQUEST.get("old_pwd")
	pwd = request.REQUEST.get("pwd")
	pwd2 = request.REQUEST.get("pwd2")
	
	if old_pwd == "":
		return commons.res_fail(1, "旧密码不能为空")
	if pwd == "":
		return commons.res_fail(1, "新密码不能为空")
	if pwd != pwd2:
		return commons.res_fail(1, "确认密码不正确")
	
	try:
		admin = Admin.objects.filter(name = curr_admin.name, pwd = old_pwd)
		admin.pwd = pwd
		admin.save()
	
		return commons.res_success("修改密码成功")
	except:
		return commons.res_fail(1, "旧密码不正确")

def ajax_art_single_get(request):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")
	
	id = request.REQUEST.get("id")
	
	obj = ArtSingle.objects.get(id = id)
	return commons.res_success("请求成功", json.loads(obj.toJSON()))

def ajax_art_single_update(request):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")
	
	id = request.REQUEST.get("id")
	content = request.REQUEST.get("content")
	
	obj = ArtSingle.objects.get(id = id)
	obj.content = content
	
	obj.save()
	return commons.res_success("更新成功")

def ajax_dataclass_list(request):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")

	dataclass_list = DataClass.objects.filter(parent_id = 0)
	dataclass_list_json = []
	for dataclass in dataclass_list:		
		item = json.loads(dataclass.toJSON())
		
		child_count = DataClass.objects.filter(parent_id = item["id"]).count()
		if child_count > 0:
			item["children"] = commons.dataclass_list(item["id"])
			
		dataclass_list_json.append(item)
	
	return commons.res_success("请求成功", dataclass_list_json)

def ajax_dataclass_get(request):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")
		
	try:
		id = request.REQUEST.get("id")
		dataclass = DataClass.objects.get(id = id)
		
		#该分类下的数据
		#test = dataclass.data_set.all()
		#print test.count()
		
		dataclass_json = json.loads(dataclass.toJSON())
		if dataclass_json["parent_id"] != 0:
			dataclass_json["parent"] = commons.dataclass_get(dataclass_json["parent_id"])
		
		return commons.res_success("请求成功", dataclass_json)
	except:
		return commons.res_fail(1, "找不到该数据")

def ajax_dataclass_add(request):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")
	
	id = 0
	if request.REQUEST.get("id"):
		id = int(request.REQUEST.get("id"))
	
	name = request.REQUEST.get("name")
	parent_id = int(request.REQUEST.get("parent_id"))
	
	dataclass = None
	if id != 0:
		dataclass = DataClass.objects.get(id = id)
	else:
		dataclass = DataClass()
	
	dataclass.name = name
	dataclass.parent_id = parent_id
	dataclass.sort = int(request.REQUEST.get("sort"))
	dataclass.type = int(request.REQUEST.get("type"))
	dataclass.save()
	
	if id != 0:
		return commons.res_success("更新成功")
	else:
		return commons.res_success("添加成功")

def ajax_dataclass_del(request):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")
	
	id = request.REQUEST.get("id")
	try:
		dataclass = DataClass.objects.get(id = id)
		
		#删除该分类下面的对应数据
		
		dataclass.delete()
		return commons.res_success("删除成功")
	except:
		return commons.res_fail(1, "该数据不存在")

def ajax_data_list(request):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")
	
	#分页索引和每页显示数
	page = 1
	if request.REQUEST.get("page"):
		page = int(request.REQUEST.get("page"))
	page_size = cfg.page_size
	if request.REQUEST.get("page_size"):
		page_size = int(request.REQUEST.get("page_size"))
	
	data_list = Data.objects.all()
	data = []
	for i in data_list:		
		item = json.loads(i.toJSON())
		data.append(item)
	
	return commons.res_success("请求成功", data)

def ajax_data_get(request):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")
		
	try:
		id = request.REQUEST.get("id")
		data = Data.objects.get(id = id)
		return commons.res_success("请求成功", json.loads(data.toJSON()))
	except:
		return commons.res_fail(1, "找不到该数据")

def ajax_data_add(request):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")
	
	id = 0
	if request.REQUEST.get("id"):
		id = int(request.REQUEST.get("id"))
	
	name = request.REQUEST.get("name")
	content = request.REQUEST.get("content")
	
	if not name or name == "":
		return commons.res_fail(1, "名称不能为空")
	elif not content or content == "":
		return commons.res_fail(1, "内容不能为空")
	
	data = None
	if id != 0:
		data = Data.objects.get(id = id)
	else:
		data = Data()
	
	data.name = name
	data.content = content
	data.add_time = int(time.time())
	data.dataclass_id = request.REQUEST.get("dataclass_id")
	data.sort = request.REQUEST.get("sort")
	data.type = request.REQUEST.get("type")
	data.hits = 0
	data.picture = ""
	data.save()
	
	if id != 0:
		return commons.res_success("更新成功")
	else:
		return commons.res_success("添加成功")

def ajax_data_del(request):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")

	id = request.REQUEST.get("id")
		
	try:
		data = Data.objects.get(id = id)
		data.delete()
		return commons.res_success("删除成功")
	except:
		return commons.res_fail(1, "该数据不存在")
