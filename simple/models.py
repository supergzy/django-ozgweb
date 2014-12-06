#coding:utf-8

from django.db import models
import json

def to_json(obj):
	fields = []
	for field in obj._meta.fields:
		fields.append(field.name)
	d = {}
	for attr in fields:
		val = getattr(obj, attr)
		
		#如果是model类型，就要再一次执行model转json
		if isinstance(val, models.Model):
			val = json.loads(to_json(val))
		d[attr] = val
	return json.dumps(d)

class Admin(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 50)
	pwd = models.CharField(max_length = 50)
	add_time = models.IntegerField(default = 0)
	
	def toJSON(self):
		return to_json(self)

class ArtSingle(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 50)
	content = models.TextField()
	
	def toJSON(self):
		return to_json(self)
	
class DataClass(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 50)
	parent_id = models.IntegerField(default = 0)
	sort = models.IntegerField(default = 0)
	type = models.IntegerField(default = 0)

	def toJSON(self):
		return to_json(self)

class Data(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 50)
	content = models.TextField()
	add_time = models.IntegerField(default = 0)
	dataclass = models.ForeignKey(DataClass)
	sort = models.IntegerField(default = 0)
	type = models.IntegerField(default = 0)
	hits = models.IntegerField(default = 0)
	picture = models.CharField(max_length = 50)

	def toJSON(self):
		return to_json(self)
