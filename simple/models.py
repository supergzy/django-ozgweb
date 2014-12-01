#coding:utf-8

from django.db import models

class Admin(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 50)
	pwd = models.CharField(max_length = 50)
	add_time = models.IntegerField()

class ArticleSingle(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 50)
	content = models.TextField()

class DataClass(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 50)
	parent_id = models.IntegerField()
	sort = models.IntegerField()
	type = models.IntegerField()

class Data(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 50)
	content = models.TextField()
	add_time = models.IntegerField()
	dataclass = models.ForeignKey(DataClass)
	sort = models.IntegerField()
	type = models.IntegerField()
	hits = models.IntegerField()
	picture = models.CharField(max_length = 50)
