---
layout: post
title: Python 的内置函数
category: project
description: 完成上一篇 Python 的内置函数的关于 Python 的类未完成部分。
---

## 一些在 Python 的类中的特殊函数

### Python 的类

在 [Python 继承中的构造方法和成员方法](https://windard.com/blog/2016/03/01/Method-In-Python-Child) 一文中已经对 Python 的类有一个简单的介绍，这里不再赘述。

### Python 的类的常见内置方法和属性

#### 类的属性

- __dict__  : 类的属性（包含一个字典，由类的数据属性组成）
- __doc__ : 类的说明文档，即定义类时的注释
- __name__ : 类的名字
- __file__ : 类所在的完整文件地址
- __bases__ : 类的父类
- __module__ : 类所在的模块

#### 实例的属性

#### 类的函数

#### 实例的函数

#### 上下文管理器

在 Python 中有一个很重要的部分即是上下文管理器，比如说我们想要计算某个函数的运行时间。

```
# coding=utf-8
import time

class ElapsedTime(object):
	def __enter__(self):
		self.start_time = time.time()

	def __exit__(self, exception_type, exception_value, traceback):
		self.end_time = time.time()
		print "Speeds %f S."%(self.end_time - self.start_time)

def countsum(count):
	num = 0
	for x in xrange(count):
		num += x
	return num

with ElapsedTime():
	print countsum(100000)		
```

这个也可以用装饰器来实现

```
# coding=utf-8
import time

def ElapsedTimeWarp(func):
	def spendtime(*args, **kwargs):
		start_time = time.time()
		result = func(*args, **kwargs)
		end_time = time.time()
		print "Speeds %f S."%(end_time - start_time)
		return result
	return spendtime

@ElapsedTimeWarp
def countsum(count):
	num = 0
	for x in xrange(count):
		num += x
	return num

print countsum(100000)
```