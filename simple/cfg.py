#coding:utf-8

web_name = "django-ozgweb"
jquery = "http://code.jquery.com/jquery-2.1.1.min.js"

#后台菜单
admin_menu_list = [
	{ 
		"id": 1, 
		"name": "后台管理", 
		"selected": True, 
		"child_menu": [
			{
				"id": 1,
				"name": "数据管理",
				"child_menu": [
					{
						"id": 1,
						"name": "分类列表",
					},
					{
						"id": 2,
						"name": "数据列表",
					},
				]
			},
			{
				"id": 2,
				"name": "区域管理",
				"child_menu": [
					{
						"id": 1,
						"name": "区域管理1",
					},
				]
			},
			{
				"id": 3,
				"name": "管理员管理",
				"child_menu": [
					{
						"id": 1,
						"name": "修改密码",
					},
					{
						"id": 2,
						"name": "管理员列表",
					},
				]
			},
		]
	},
	{ "id": 2, "name": "测试菜单1"},
	{ "id": 3, "name": "测试菜单2"},
	{ "id": 4, "name": "测试菜单3"},
]
