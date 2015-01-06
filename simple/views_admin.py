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
	
	return commons.render_template(request, "admin/index.html")

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
	
	return commons.render_template(request, "admin/admin.html", res_data)

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

	res_data = Admin.getList(page, page_size)
	
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
		admin = Admin.objects.get(name = curr_admin["name"], pwd = old_pwd)
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
	
	type = int(request.REQUEST.get("type"))
	dataclass_list = DataClass.objects.filter(type = type, parent_id = 0).order_by("-sort", "-id")
	dataclass_list_json = []
	for dataclass in dataclass_list:		
		item = json.loads(dataclass.toJSON())
		
		child_count = DataClass.objects.filter(parent_id = item["id"]).count()
		if child_count > 0:
			item["children"] = DataClass.listById(item["id"])
			
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
			dataclass_json["parent"] = DataClass.getById(dataclass_json["parent_id"])
		
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
		if id == parent_id:
			return commons.res_fail(1, "父级分类不能为当前选中分类")
		
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
		
		child_count = DataClass.objects.filter(parent_id = dataclass.id).count()
		if child_count > 0:
			DataClass.deleteById(dataclass.id)
		
		#删除该分类下面的对应数据
		Data.objects.filter(dataclass_id = dataclass.id).delete()
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
	
	type = int(request.REQUEST.get("type"))
	
	res_data = Data.getList(page, page_size, type)
	return commons.res_success("请求成功", res_data)

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
		data.hits = 0
		data.add_time = int(time.time())
	
	data.name = name
	data.content = content	
	data.dataclass_id = int(request.REQUEST.get("dataclass_id"))
	data.sort = int(request.REQUEST.get("sort"))
	data.type = int(request.REQUEST.get("type"))	
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

	id = int(request.REQUEST.get("id"))
		
	try:
		data = Data.objects.get(id = id)
		data.delete()
		return commons.res_success("删除成功")
	except:
		return commons.res_fail(1, "该数据不存在")
