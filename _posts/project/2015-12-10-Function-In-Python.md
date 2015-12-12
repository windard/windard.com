---
layout: post
title: python的内置函数
category: project
description: 强大的Python不仅有面向对象的特性，而且有很多强大的内置函数。
---

Python的内置函数主要包括两大类，一是Python的函数式编程用到的函数，一是Python对象的内置函数。                      

##函数式编程

##Python的序列里支持函数表达。   

```python
>>> a = [x for x in range(10)]
>>> a
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> a = [x**2 for x in range(10)]
>>> a
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
>>> a = [x**3 for x in range(10) if x%3]
>>> a
[1, 8, 64, 125, 343, 512]
>>> a = [(x,y) for x in range(3) for y in range(5)]
>>> a
[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4)]
>>> from random import randint
>>> nums = [randint(1,10) for i in range(2)]
>>> nums
[3, 6]
```     

这是列表解析，同样的，字典也支持这样的解析。                   

```python
>>> a
{'a': 10, 'b': 20}
>>> a = {1:'one',2:'two',3:'three'}
>>> b = {key:value for (key,value) in a.items() }
>>> b
{1: 'one', 2: 'two', 3: 'three'}
>>> b = {key:value for (key,value) in a.items() if key%2}
>>> b
{1: 'one', 3: 'three'}
>>> a = {key:value for key in range(1,4) for value in range(5) if value%key}
>>> a
{2: 3, 3: 4}
>>> a = {key:value for key in range(5) for value in range(5) if value>key}
>>> a
{0: 4, 1: 4, 2: 4, 3: 4}
>>> a = {key:value for key in range(5) for value in range(5) if value==key}
>>> a
{0: 0, 1: 1, 2: 2, 3: 3, 4: 4}
```

在这里，因为Python的字典的键具有互异性，所以每一次相同的键不同的值只会取最后一个，而列表无互异性。                        

```python
>>> [(key,value) for key in range(5) for value in range(5) if value>key]
[(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
>>> {key:value for key in range(5) for value in range(5) if value>key}
{0: 4, 1: 4, 2: 4, 3: 4}
```

##Python函数支持不定长度的参数
用一个C语言里很经典的例子，求一个不定长度的数列的和。

```python
#coding=utf-8

def count(*args):
	num = 0
	for i in args:
		num += i
	return num

num = count(1,2,3)
print num

num = count(1,2,3,4,5,6)
print num

a = [1,2,3,4]
num = count(*a)
print num
```

保存为count.py，运行，看一下结果。                        
![count.jpg](../../images/count.jpg)

不仅仅是对列表类型的支持，字典也可以。                     

```python
#coding=utf-8

def echo(**arge):
	for (i,j) in arge.items():
		print i,j

echo(a="one",b="two")

#此处的键值不能为数字,必须为是一个变量
# echo(1="one",2="two")

echo(**{"1":"one","2":"two","3":"three"})

#此处的键值也不能为数字，必须是字符串
# echo(**{1:"one",2:"two",3:"three"})
```

保存为count_dict.py，运行，看一下结果。                        
![count_dict.jpg](../../images/count_dict.jpg)                   

##Python 不再支持自加自减
在C语言或者是其他的大部分语言，自加自减都是很重要的一个运算符，但是可能是为了减少像`++i`和`i++`的歧义吧，反正是没有了。                                  
所以在Python里面`i++`会报错，而`++i`则没有任何反应，无论你在前面有多少个加号都没有任何反应`++++i`                                      

```python
>>> i = 0
>>> i++
  File "<stdin>", line 1
    i++
      ^
SyntaxError: invalid syntax
>>> i++++
  File "<stdin>", line 1
    i++++
        ^
SyntaxError: invalid syntax
>>> ++i
0
>>> ++++i
0
```

但是可能是弥补没有自加的缺陷吧，Python可以`**`，表示乘方。              

```python
>>> 2**3
8
>>> 3**2
9
```

还有另外一个惊人的特性，关于两个变量值的对换。                         

```python
>>> a = 1
>>> b = 2
>>> a,b = b,a
>>> a
2
>>> b
1
```

##help和__doc__
这两个是函数的内置函数，就是说每一个函数都会有这两个函数，实际上也可以用于函数库或者是Python对象中。                                                   
他们的功能是查看该函数或者是函数库的说明文档。说明文档即函数声明之后第一个未被赋值的字符串，一般用`""`或者是`""""""`包围的部分。                            

```python
>>> def foo():
...     "This is for test function"
...     pass
...
>>> help(foo)
Help on function foo in module __main__:

foo()
    This is for test function

>>> foo.__doc__
'This is for test function'
>>> a = help(foo)
Help on function foo in module __main__:

foo()
    This is for test function

>>> print a
None
>>> b = foo.__doc__
>>> print b
This is for test function
```

可以看到它们虽然功能一样，但是也有少许的不同之处。
1. `help`不仅仅打印出了说明文档，还有一些函数的参数以及函数所在的主类等全部信息。`__doc__`则仅打印出说明文档。                        
2. `help`无返回值，直接打印出结果。`__doc__`返回一个字符串。

这两个函数在一些类库的学习中很有帮助，可以用来查看说明文档以及相关函数的参数。       

```python
>>> import urllib
>>> help(urllib)
Help on module urllib:

NAME
    urllib - Open an arbitrary URL.

FILE
    c:\python27\lib\urllib.py

DESCRIPTION
    See the following document for more info on URLs:
    "Names and Addresses, URIs, URLs, URNs, URCs", at
    http://www.w3.org/pub/WWW/Addressing/Overview.html

    See also the HTTP spec (from which the error codes are derived):
    "HTTP - Hypertext Transfer Protocol", at
    http://www.w3.org/pub/WWW/Protocols/

    Related standards and specs:
    - RFC1808: the "relative URL" spec. (authoritative status)
    - RFC1738 - the "URL standard". (authoritative status)
    - RFC1630 - the "URI spec". (informational status)

    The object returned by URLopener().open(file) will differ per
    protocol.  All you know is that is has methods read(), readline(),
    readlines(), fileno(), close() and info().  The read*(), fileno()
    and close() methods work like those of open files.
    The info() method returns a mimetools.Message object which can be
    used to query various info about the object, if available.
    (mimetools.Message objects are queried with the getheader() method.)

CLASSES
    URLopener
        FancyURLopener

    class FancyURLopener(URLopener)
     |  Derived class with handlers for errors we can handle (perhaps).
     |
     |  Methods defined here:
     |
     |  __init__(self, *args, **kwargs)

>>> urllib.__doc__
'Open an arbitrary URL.\n\nSee the following document for more info on URLs:\n"Names and Addresses, URIs, URLs, URNs, URCs"
 spec (from which the error codes are derived):\n"HTTP - Hypertext Transfer Protocol", at\nhttp://www.w3.org/pub/WWW/Protoc
thoritative status)\n- RFC1738 - the "URL standard". (authoritative status)\n- RFC1630 - the "URI spec". (informational sta
ol.  All you know is that is has methods read(), readline(),\nreadlines(), fileno(), close() and info().  The read*(), file
eturns a mimetools.Message object which can be\nused to query various info about the object, if available.\n(mimetools.Mess
>>> help(urllib.urlopen)
Help on function urlopen in module urllib:

urlopen(url, data=None, proxies=None, context=None)
    Create a file-like object for the specified URL to read from.

>>> urllib.urlopen.__doc__
'Create a file-like object for the specified URL to read from.'
>>>
```

当说明文档太长时，按`q`退出。                        
可以用`help`查看具体用法，用`__doc__`查看相关说明。                

####内嵌函数
在Python里面一个函数内部可以创建另一个函数并调用它，当然也只能在这个函数内部使用。

```python
>>> def foo():
...     print "foo"
...     def bar():
...             print "bar"
...     bar()
...
>>> foo()
foo
bar
>>> bar()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'bar' is not defined
```

####函数装饰器
装饰器实际上也是函数

####匿名函数
匿名函数的关键字是lambda

####apply filter map reduce

######apply(function,arges)
apply的功能是在不定长参数的函数中应用，在我们上面讲到不定长参数的使用时，传入一个序列或者字典时可以采用加`*`或者是`**`的形式，将序列传入函数，也可以采用apply。                       
其实不仅仅是不定长参数的函数，及时是在定长参数的函数中，如果需要多个参数也能使用。       
apply或者`*`,`**`是为了一次性传入一个列表或者字典，但是将它们内部的值逐个解析出来。       
在Python 1.6 之后，这个函数将被逐步取代，apply只能传入序列。                          

```python
#coding=utf-8

def count(*args):
  num = 0
  for i in args:
    num += i
  return num

num = apply(count,[1,2,3])
print num

a = [1,2,3,4,5,6]
num = apply(count,a)
print num
```

保存为count_apply.py，运行，看一下结果。                                     
![count_apply.jpg](../../images/count_apply.jpg)

####

####apply map 
##对象内置函数

包括`__name__` `__call__` `__init__` `__name__`
