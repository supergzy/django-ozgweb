#coding:utf-8

import commons
import cfg
import json
import time
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
		"title": cfg.web_name
	}

	return commons.render_template(request, "admin/index.html", res_data);

def admin(request):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return HttpResponseRedirect("index")
	
	res_data = {
		"title": cfg.web_name
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

def ajax_admin_list(request):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")
	
	admin_list = Admin.objects.all()
	return commons.res_success("请求成功", admin_list)

def ajax_admin_add(request):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")
	
	name = request.REQUEST.get("name")
	pwd = request.REQUEST.get("pwd")
	
	total = Admin.objects.filter(name = name).count()
	if total > 0:
		return commons.res_fail(1, "该管理员已存在")
	
	admin = Admin(
		name = name,
		pwd = pwd,
		add_time = int(time.time())
	)
	admin.save()
	
	return commons.res_success("添加成功", admin)

def ajax_admin_del(request, id):
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
	
	if pwd != pwd2:
		return commons.res_fail(1, "确认密码不正确")
	
	try:
		admin = Admin.objects.filter(name = curr_admin.name, pwd = old_pwd)
		admin.pwd = pwd
		admin.save()
	
		return commons.res_success("修改密码成功")
	except:
		return commons.res_fail(1, "旧密码不正确")

def ajax_art_single_get(request, id):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")
	
	art = ArtSingle.objects.get(id = id)
	return commons.res_success("请求成功", json.loads(atr.toJSON()))
	
def ajax_art_single_update(request):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")
	
	id = request.REQUEST.get("id")
	content = request.REQUEST.get("content")
	
	art = ArtSingle.objects.get(id = id)
	art.content = content
	
	art.save()
	return commons.res_success("更新成功")

def ajax_dataclass_list(request):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")

	dataclass_list = Admin.objects.filter(parent_id = 0)
	return commons.res_success("请求成功", dataclass_list)

def ajax_dataclass_get(request, id):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")
		
	try:
		dataclass = DataClass.objects.get(id = id)
		return commons.res_success("请求成功", json.loads(data.toJSON()))
	except:
		return commons.res_fail(1, "找不到该数据")

def ajax_dataclass_add(request, id = 0):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")
	
	name = request.REQUEST.get("name")
	parent_id = request.REQUEST.get("parent_id")
	
	dataclass = None
	if id != 0:
		dataclass = DataClass.objects.get(id = id)
	else:
		dataclass = DataClass()
	
	dataclass.name = name
	dataclass.parent_id = parent_id
	data.sort = request.REQUEST.get("sort")
	data.type = request.REQUEST.get("type")
	data.save()
	
	if id != 0:
		return commons.res_success("更新成功")
	else:
		return commons.res_success("添加成功")

def ajax_dataclass_del(request, id):
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

def ajax_data_list(request, page = 1, page_size = 10):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")
	
	data_list = Data.objects.all()
	data = []
	for i in data_list:		
		item = json.loads(i.toJSON())
		data.append(item)
	
	return commons.res_success("请求成功", data)

def ajax_data_get(request, id):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")
		
	try:
		data = Data.objects.get(id = id)
		return commons.res_success("请求成功", json.loads(data.toJSON()))
	except:
		return commons.res_fail(1, "找不到该数据")

def ajax_data_add(request, id = 0):
	#需要登录才可以访问
	if not request.session.get("sess_admin", False):
		return commons.res_fail(1, "需要登录才可以访问")
	
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

def ajax_data_del(request, id):
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
