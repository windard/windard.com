---
layout: post
title: 遍历Python中的字典
category: project
description: 方法有很多，简单记录一下。
---

## 遍历字典


```python
# coding=utf-8

a = {'a':"hello",1:90,'3':'world','hehe':'nihao'}

# 第一种方法
for i in a:
	print str(i) +" : " + str(a[i])

# 第二种办法
for i in a.items():
	print str(i[0]) + " : " + str(i[1])

# 第三种方法
for i,j in a.items():
	print str(i) + " : " + str(j)

# 第四种方法
for i in a.keys():
	print str(i) + " : " + str(a[i])

# 第五种方法
for i,j in enumerate(a.values()):
	print str(i) + " : " + str(j)

# 第六种方法
for i in zip(a.keys(),a.values()):
	print str(i[0]) + " : " + str(i[1])

# 第七种方法
for i,j in a.iteritems():
	print str(i) + " : " + str(j)

# 第八种方法
for i,j in zip(a.iterkeys(),a.itervalues()):
	print str(i) + " : " + str(j)
```