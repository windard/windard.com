---
layout: post
title: Python打开txt文件中读取的文件目录里的文件
category: project
description: 关于字符编码各种问题，至今尚未解决，求帮助~~
---

用Python打开txt文件中读取的文件目录里的文件，明明现在读取出来的文件目录已经是utf-8编码了，用open打不开。

于是开始各种转码，包括目录文件的编码也改了，读取出来的文件目录是Unicode编码都打不开，codecs也不行，不知道什么鬼，现在将问题完完整整的列下来，希望有人能帮助解答，或者自己以后没准看看就会了。。

现在目录文件是`list.txt`，内容如下：  
```
C:\Users\dell\Desktop\Document\人事处\2-141125143603西安电子科技大学2015年非教师岗位招聘需求计划.docx   
C:\Users\dell\Desktop\Document\人事处\2011以前年度考核登记表.docx   
C:\Users\dell\Desktop\Document\人事处\2012-2013年度考核登记表.doc   
C:\Users\dell\Desktop\Document\人事处\2014年“千人计划”项目意向人选推荐表.docx   
C:\Users\dell\Desktop\Document\人事处\2014年度岗位津贴拟调整人员名单样表.xls   
C:\Users\dell\Desktop\Document\人事处\2014年度年度考核登记表（教师）.doc   
C:\Users\dell\Desktop\Document\人事处\2014年度年度考核登记表（非教师）.doc   
C:\Users\dell\Desktop\Document\人事处\2014年考核相关表格.rar   
...   
```
还有很多，都是这样的文件目录，刚开始的时候，用的是GBK的编码方式存储的，但是可以在读取出来之后转码为Unicode编码，可是同样打不开。  
先尝试一下，直接提取一个目录文件出来，打开文件是可以的，代码如下：  
```python
#coding=utf-8
file1 = r"C:\Users\dell\Desktop\Document\人事处\2-141125143603西安电子科技大学2015年非教师岗位招聘需求计划.docx".decode("utf-8")
filename = open(file1, 'rb')
filename.close()
```
这样是可以的，但是同样的文件路径，我从txt文件中读取出来的就不行，像下面这样。
```python
#coding=utf-8
justfile = open('list.txt','r')
allfile = []
while 1:
	line = justfile.readline()
	line.strip()
	allfile.append(line)
	if not line:
		break
file1 = allfile[0].decode('gbk')
filename = open(file1, 'rb')
filename.close()
```
不行，报错。   
```
IOError: [Errno 22] invalid mode ('rb') or filename: u'C:\\Users\\dell\\Desktop\\Document\\\u4eba\u4e8b\u5904\\2-141125143603\u897f\u5b89\u7535\u5b50\u79d1\u6280\u5927\u5b662015\u5e74\u975e\u6559\u5e08\u5c97\u4f4d\u62db\u8058\u9700\u6c42\u8ba1\u5212.docx\n'
```
从错误原因中可以看出来，文件路径已经被转化为了Unicode编码格式，那难道是open不能打开Unicode编码格式的？我们将它解码为utf-8试试。   
```python
#coding=utf-8
justfile = open('list.txt','r')
allfile = []
while 1:
	line = justfile.readline()
	line.strip()
	allfile.append(line)
	if not line:
		break
file1 = allfile[0].decode('gbk').encode("utf-8")
filename = open(file1, 'rb')
filename.close()
```
仍然是有问题。   
```
IOError: [Errno 22] invalid mode ('rb') or filename: 'C:\\Users\\dell\\Desktop\\Document\\\xe4\xba\xba\xe4\xba\x8b\xe5\xa4\x84\\2-141125143603\xe8\xa5\xbf\xe5\xae\x89\xe7\x94\xb5\xe5\xad\x90\xe7\xa7\x91\xe6\x8a\x80\xe5\xa4\xa7\xe5\xad\xa62015\xe5\xb9\xb4\xe9\x9d\x9e\xe6\x95\x99\xe5\xb8\x88\xe5\xb2\x97\xe4\xbd\x8d\xe6\x8b\x9b\xe8\x81\x98\xe9\x9c\x80\xe6\xb1\x82\xe8\xae\xa1\xe5\x88\x92.docx\n'
```
现在从错误里面可以看到文件编码格式已经是utf-8格式的了，而且如果此时增加一个输出，在sublime上能够正常显示，即说明确实是utf-8编码，但是为什么还是打不开呢？   
那接下来我们试一下用codecs来打开文件，还是以上两种格式，试一下。   
```python
#coding=utf-8
import codecs
file1 = r"C:\Users\dell\Desktop\Document\人事处\2-141125143603西安电子科技大学2015年非教师岗位招聘需求计划.docx".decode("utf-8")
filename = codecs.open(file1 , "rb")
filename.close()
```
同样的，这个能打开，正常不报错。   
```python
#coding=utf-8
import codecs
justfile = open('list.txt','r')
allfile = []
while 1:
	line = justfile.readline()
	line.strip()
	allfile.append(line)
	if not line:
		break
file1 = allfile[0].decode('gbk').encode("utf-8")
filename = codecs.open(file1 , "rb")
filename.close()
```
打不开，报错。   
```
IOError: [Errno 22] invalid mode ('rb') or filename: 'C:\\Users\\dell\\Desktop\\Document\\\xe4\xba\xba\xe4\xba\x8b\xe5\xa4\x84\\2-141125143603\xe8\xa5\xbf\xe5\xae\x89\xe7\x94\xb5\xe5\xad\x90\xe7\xa7\x91\xe6\x8a\x80\xe5\xa4\xa7\xe5\xad\xa62015\xe5\xb9\xb4\xe9\x9d\x9e\xe6\x95\x99\xe5\xb8\x88\xe5\xb2\x97\xe4\xbd\x8d\xe6\x8b\x9b\xe8\x81\x98\xe9\x9c\x80\xe6\xb1\x82\xe8\xae\xa1\xe5\x88\x92.docx\n'
```
再试一个。   
```python
#coding=utf-8
import codecs
justfile = open('list.txt','r')
allfile = []
while 1:
	line = justfile.readline()
	line.strip()
	allfile.append(line)
	if not line:
		break
file1 = allfile[0].decode('gbk')
filename = codecs.open(file1 , "rb")
filename.close()
```
这样也打不开，接着报错。   
```
IOError: [Errno 22] invalid mode ('rb') or filename: u'C:\\Users\\dell\\Desktop\\Document\\\u4eba\u4e8b\u5904\\2-141125143603\u897f\u5b89\u7535\u5b50\u79d1\u6280\u5927\u5b662015\u5e74\u975e\u6559\u5e08\u5c97\u4f4d\u62db\u8058\u9700\u6c42\u8ba1\u5212.docx\n'
```
难道时候一开始的目录文件有问题？我们来试一下utf-8的目录文件，同样的内容，保存为`test.txt`。   
```python
#coding=utf-8
import codecs
justfile = open('test.txt','r')
allfile = []
while 1:
	line = justfile.readline()
	line.strip()
	allfile.append(line)
	if not line:
		break
file1 = allfile[0]
filename = open(file1, 'rb')
filename.close()
```
一开始我们连目录路径的编码格式转换都没有，果然报错。   
```
IOError: [Errno 22] invalid mode ('rb') or filename: '2-141125143603\xe8\xa5\xbf\xe5\xae\x89\xe7\x94\xb5\xe5\xad\x90\xe7\xa7\x91\xe6\x8a\x80\xe5\xa4\xa7\xe5\xad\xa62015\xe5\xb9\xb4\xe9\x9d\x9e\xe6\x95\x99\xe5\xb8\x88\xe5\xb2\x97\xe4\xbd\x8d\xe6\x8b\x9b\xe8\x81\x98\xe9\x9c\x80\xe6\xb1\x82\xe8\xae\xa1\xe5\x88\x92.docx'
```
那我们加一个编码格式上去。   
```python
#coding=utf-8
import codecs
justfile = open('test.txt','r')
allfile = []
while 1:
	line = justfile.readline()
	line.strip()
	allfile.append(line)
	if not line:
		break
file1 = allfile[0].decode("utf-8")
filename = open(file1, 'rb')
filename.close()
```
依然没有什么卵用，报错如下。   
```
IOError: [Errno 2] No such file or directory: u'2-141125143603\u897f\u5b89\u7535\u5b50\u79d1\u6280\u5927\u5b662015\u5e74\u975e\u6559\u5e08\u5c97\u4f4d\u62db\u8058\u9700\u6c42\u8ba1\u5212.docx'
```
发现一个问题，是不是我的之前一个文件打开没有关上的原因，那我就把之前的那个关上再试试。   
```python
#coding=utf-8
import codecs
justfile = open('test.txt','r')
allfile = []
while 1:
	line = justfile.readline()
	line.strip()
	allfile.append(line)
	if not line:
		break
file1 = allfile[0].decode("utf-8")
justfile.close()
filename = open(file1, 'rb')
filename.close()
```
同样的错误。而且其实同时打开两个不同名的文件是可以的，如下。   
```python
file1 = open("test.txt","r")
file2 = open("list.txt","r")
file1.close()
file2.close()
```
这个是可以的。   

那这次就是utf-8编码格式的也打不开，然后用utf-8格式的`test.txt`重复了之前的代码，报错一模一样，都不可以，那只能由此得出一个暂时性我个人的结论，如果文件名是有文件里读取出来的，无论如何都不能被打开这个文件。  

