---
layout: post
title: python网络爬虫
category: project
description: 网络爬虫，即Web Spider，抓取网页数据，像Google，Baidu等公司，他们的搜索引擎每天都派出数以亿万的爬虫夜以继日的抓取网络数据并存储起来，无数的网络工程师为他们的抓取速度，存储效率做优化。
---

#python网络爬虫

---
[TOC]


##关于爬虫
网络爬虫，即Web Spider，抓取网页数据，像Google，Baidu等公司，他们的搜索引擎每天都派出数以亿万的爬虫夜以继日的抓取网络数据并存储起来，无数的网络工程师为他们的抓取速度，存储效率做优化。

当然他们的爬虫不是用python写的，不过python强大的各种函数库的使用也可以做简单的爬虫来玩玩。本系列教程博客主要使用的python库有urllib urllib2 request re和cookielib。因为python2.x与python3.x有一定区别，特作强调，本系列博客使用的是python2.7.10。

##urllib

####基本使用
urllib是几乎所有的python网络爬虫都会使用的库，功能很简单直接，向指定URL发送http请求并接受数据，以下是一个urllib基本实例。 

```python
# coding=utf-8
#导入urllib库
import urllib
#设定将要请求的URL地址
url = 'http://www.baidu.com'
#其实重点就这一句
page = urllib.urlopen(url)
#读取接收到的数据
html = page.read()
#打印接受到的数据
print html
```

保存为urllib_demo.py,运行。如果你得到的是一堆类似于这种的密密麻麻的数据，就说明urllib请求和接收正常。
![BAIDU源码](baidu.jpg)

可以看出来urllib库的主要函数就是urlopen()，其实跟基本的文件操作很类似，open打开一个文件，然后用read()读取文件内容，所以也能用readline()来单行读取文件内容。

####进阶操作

######发送请求
urlopen的可选参数当然不止一个，比如说或许我们需要在http中同时发送get或者post请求，我们就需要一个参数params或者data，params是get请求的参数，data是post请求的数据，同时我们还需要一个函数，urlencode，将我们的参数进行封装。

1. GET请求
在这里我们使用我本地服务器上一个小例子来演示一下，GET请求的页面代码如下，保存在根目录下，命名为form_get.php。
```php
<?php 
    $NAME = $_GET['name'];
    $EMAIL = $_GET['email'];
    if($NAME == 'admin'){
        echo "Welcome Back ";
        echo "Your Email : ".$EMAIL;
    }else{
        echo "Get Out !";
    }
?>
```
然后就是我们的python发送get请求：
```python
import urllib
params = urllib.urlencode({'name':'admin','email':'me@wenqiangyang.com'})
page = urllib.urlopen("http://localhost/form_get.php?%s" % params)
html = page.read()
print html
```
保存为urllib_get.py,运行，看一下接收回来的数据。
![GET请求](get.jpg)
在此处也可以采用另一种的写法：
```python
import urllib
url = 'http:localhost/form_get.php'
params = urllib.urlencode({'name':'admin','email':'me@wenqiangyang.com'})
page = urllib.urlopen(url+'?'+params)
html = page.read()
print html
```
仔细分析一下代码就可以看出来%s是将params内的参数直接加到了URL的后面来仿制一个get请求，那么post请求该如何处理呢？post的数据并不在URL上的吖。

2. POST请求
本地服务器上POST请求的页面代码如下，同样保存在根目录下，命名为form_post.php。
```php
<?php 
	$NAME = $_POST['name'];
	$EMAIL = $_POST['email'];

	if($NAME == 'admin'){
		echo "Welcome Back ";
		echo "Your Email : ".$EMAIL;
	}else{
		echo "Get Out !";
	}
?>
```
然后就是我们的python发送post请求：
```python
import urllib
params = urllib.urlencode({'name':'windard','email':'1106911190@qq.com'})
page = urllib.urlopen("http://localhost/form_post.php",params)
html = page.read()
print html
```
保存为urllib_post.py,运行，看一下接收回来的数据。
![POST请求](post.jpg)
仔细分析一下源码可以看出来，urlopen的第一个参数已经出现了，就是params可以在发送http请求是附带其他数据或者参数，来实现不同的http请求。
urllib除了可以发送简单get和post请求，还可以发送put和delect请求，这两种比较复杂，这里就不在做详细讲解了。

######urlopen返回对象的其他操作
前面已经说到，urlopen的操作与文件的基本操作类似，但是urlopen返回的对象除了基本的读取操作之外还有一些其他的操作。

**urlopen返回对象提供方法：**
- read() , readline() ,readlines() , fileno() , close() ：这些方法的使用方式与文件对象完全一样
- info()：返回一个httplib.HTTPMessage对象，表示远程服务器返回的头信息
- getcode()：返回Http状态码。如果是http请求，200请求成功完成;404网址未找到
- geturl()：返回请求的url

我们来试一下，还是以百度为例：
```python
# coding=utf8
#导入urllib库
import urllib
#设定将要请求的URL地址
url = 'http://www.baidu.com'
#其实重点就这一句
page = urllib.urlopen(url)
#读取接收到的返回信息
info = page.info()
#打印出来
print "Info:"
print info
#读取接收到的返回状态码
code = page.getcode()
#打印出来
print "Code:"
print code
```
保存为urllib_info.py，运行，看一下结果。
![urllib返回值](info.jpg)
可以看到http请求返回的信息，还有表示请求成功的200状态码。

######urllib.urlretrieve()
这有一个很实用的函数，它的功能是将URL定位的文件下载到本地，可不仅仅是html哦，这里我们直接给出它相应的需要的参数。
**urllib.urlretrieve(url[,filename[,reporthook[,data]]])**
- url：需要下载的文件的url
- filename：下载了之后保存在本地的名称
- reporthook：执行完了之后的回调函数
- data：跟url传输过去的参数
如果不指定filename，则会存为临时文件。

**urlretrieve()返回一个二元组(filename,mine_hdrs)**
- filename：传入参数的filename，保存在本地的文件名
- mine_hdrs：文件的基本信息


让我们来下载一个本地服务器的照片到python文件所在的文件夹。
照片是这样的：
![服务器上的照片](xidian_server.jpg)
python代码如下：
```python
import urllib
url = 'http://localhost/112/images/xidian.jpg'
pic = urllib.urlretrieve(url,'xidian.jpg')
print pic[0]
print pic[1]
```
保存为urllib_urlretrieve.py,运行，看一下结果。
![urlretrieve结果](urlretrieve.jpg)
确实是返回文件名和文件信息，看一下文件夹，也保存下来了xidian.jpg这个照片。
这里有一个小技巧，就是文件名的设定。
我不是指定文件名了么，在url里面，不想早后面再自己手动的写文件名了，就可以这样写：
```
pic = urllib.urlretrieve(url,url.split('/')[-1])
```
将URL按'\'截断，取最后一个字符串，即是我们想要的文件名。

####urllib其他函数
1. urllib.urlcleanup()
前面说到urllib.urlretrieve()下载指定url的文件如果不指定保存文件名的话就会存为临时文件，在缓存里，那么这个函数就是清除这里产生的缓存。

2. urllib.quote(url)和urllib.quote_plus(url)
将url数据获取之后，并将其编码，从而适用与URL字符串中，使其能被打印和被web服务器接受。
简单的看一下效果。
```
>>>import urllib
>>> urllib.quote('http://www.baidu.com')
'http%3A//www.baidu.com'
>>> urllib.quote_plus('http://www.baidu.com')
'http%3A%2F%2Fwww.baidu.com'
```

3. urllib.unquote(url)和urllib.unquote_plus(url)
与上一个函数功能相反，将编码后的url还原。

那么到这里我们的urllib函数就讲完了，是不是功能很强大呢？别担心，还有更强大的呢~

##urllib2

####基本使用
urllib2作为urllib的升级版，基本功能和使用是和urllib一致的，也可以用urlopen来发送一个请求，如下所示：
```python
import urllib2
url = 'http://www.baidu.com'
page = urllib2.urlopen(url)
html = page.read()
print html
```
保存为urllib2_demo.py,运行，看一下结果。
![urllib2_baidu_HTML](urllib2_baidu.jpg)
可以看到跟urllib的基本写法一致，返回结果也一致。

但是这只是看起来一致而已，如果我们去翻看官方手册的话就会看到其实它们的参数有一定的不同。`urllib.urlopen(url[,data[,proxies]])`和`urlopen (url [,data [,timeout]])`虽然前两个参数都是http请求地址URL和传输的数据data，但是第三个参数由没什么用的proxies换为了超时时间timeout，即在中断连接前尝试的时间，这样的话可以设定http请求如果超过多长时间就放弃，避免长时间的等待，浪费网络资源。

####进阶操作
######urllib2.Request()
既然urllib2是urllib的升级版，那么它肯定有不同于urllib的地方，那就是它引入了一个新的函数Request()，让我们来看一下Request()的使用。
它的功能是将你的http请求更加实例化，让http请求更加饱满，伪装成一个真正的浏览器发送的请求。因为有的站点为了避免被恶意的网络爬虫抓取，会对发送过来的http请求做一定的删选。
```python
#coding=utf-8
import urllib2
url = 'http://www.baidu.com'
#加入http请求的请求者地址，此处是本人的chrome 45.0.2454.12
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.12 Safari/537.36'
#封装成http请求头
headers = {'User-Agent':user_agent}
#将http请求头加入到Request中，组装成一个完整的请求
req = urllib2.Request(url=url,headers=headers)
#此时urlopen就不再是直接请求URL了，而是请求已经封装好了的Req对象
page = urllib2.urlopen(req)
html = page.read()
print html
```
保存为urllib2_request.py，运行，看一下结果。
![urllib2_baidu_HTML2](urllib2_baidu2.jpg)
显得并没有什么区别，当然没有什么区别，百度对headers并不敏感，但是起码说明这个语法是正确的，那么接下来就让我们来看一下这个函数到底有哪些参数。
（当然在headers里面也远不仅仅只有User-Agent这一个参数，但这个参数是必选参数，当然也还有一些其他的参数。）
**Request (url [data,headers [,origin_req_host ,[unverifiable]]]])**
- URL：统一资源定位符，即http请求的网址
- data：请求过程中传输的数据，用于POST请求
- header：http请求头
- origin_req_host：原始请求地址
- unverifiable：不知道是什么东西的东西

一般常用到的是前三个，现在我们用urllib2来重新实现一个post请求，还是请求本地服务器环境的form_post.php。
```python
import urllib2
import urllib
url = 'http://localhost/form_post.php'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.12 Safari/537.36'
value = {'name':'admin','email':'me@wenqiangyang.com'}
data  = urllib.urlencode(value)
headers = {'User-Agent':user_agent}
req = urllib2.Request(url,data,headers)
page = urllib2.urlopen(req)
html = page.read()
print html
```
保存为urllib2_post.py，运行，看一下结果。
![urllib2_POST](urllib2_post.jpg)
确实可以发送一个带着http请求头的post请求，虽然看不出来与之前有什么区别。
那么既然可以发送post请求，那么用之前的第二种方法发送get请求当然也可以，这里就不再做演示了。

######urllib2.build_opener()
基本的urlopen()函数不支持验证、cookie或其他HTTP高级功能。要支持这些功能，必须使用build_opener()函数来创建自己的自定义Opener对象
####urllib2其他函数
1. urllib2设置代理
2. urllib2检测重定向
3. urllib2设定cookie
4. urllib2打开错误日志

##requests
####基本使用
requests库是基于urllib的，但是它比urllib更方便，更强大，让我们看一下它的基本使用：
```python
#coding=utf-8
import requests
url  = 'http://localhost/112/index.html'
page = requests.get(url)
html = page.content
print html
```
跟urllib一样的简洁而又强大，短短的几行代码就可以构造一个http请求。

####进阶操作
######requests请求
但是它和urllib又有不同之处，urllib默认的是发送get请求，但是requests需要指定发送哪种请求，看似更加复杂，但是其实让我们获得更多的选择更便利。requests支持GET/POST/PUT/DELETE/HEAD/OPTIONS等请求类型，它们的使用也非常方便。
```
>>> r = requests.get("http://httpbin.org/get")
>>> r = requests.post("http://httpbin.org/post")
>>> r = requests.put("http://httpbin.org/put")
>>> r = requests.delete("http://httpbin.org/delete")
>>> r = requests.head("http://httpbin.org/get")
>>> r = requests.options("http://httpbin.org/get")
```
>KISS -- Keep　It　Simple  Stupid
>一切本该如此简单

那么既然可以发送GET或者POST请求，那它们的参数在哪里呢？
就在requests()的第二个和第三个参数，第二个参数params，第三个参数data，分别用来接收get和post的数据。
我们还是来试一下发送请求给本地服务器看一下结果怎么样，还是form_get.php和form_post.php.php。
```python
import requests
get_url  = 'http://localhost/form_get.php'
get_params = {'name':'admin','email':'me@wenqiangyang.com'}
post_url = 'http://localhost/form_post.php'
post_params = {'name':'windard','email':'1106911190@qq.com'}
get  = requests.get(url=get_url,params=get_params)
post = requests.post(url=post_url,data=post_params)
get_html = get.content
post_html = post.content
print get_html
print post_html
```
保存为requests.request.py,运行，看一下结果。
![requests_request](requests_request.jpg)
确实都能够成功的发送相应的请求。













  
