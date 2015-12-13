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
装饰器实际上也是函数，它的功能是在类或者是函数运行之前或者是之后运行一些额外的代码。      
装饰器的使用也是与普通函数一致，让我们来试一下，首先是一个无参的装饰器，在代码执行前后加上执行时间。                             

```python
#coding=utf-8

from time import ctime,sleep

def timefun(func):
  print ctime()
  return func

@timefun
def foo():
  print "This is foo"

for i in range(3):
  foo()
  sleep(2)

print "-"*20
timefun(foo)

print "-"*20
timefun(foo)()
```

保存为decorator_demo.py，运行，看一下结果。                        
![decorator_demo.jpg](../../images/decorator_demo.jpg)           

非常可惜的是，如果这样写的话，这个装饰器好像就只能使用一次，那我们想要在每一次调用的时候都打印出时间要怎么办呢？。                            
我们在装饰器里也定义了一个函数，使用内嵌函数就可以实现每次调用装饰器都打印出时间。        

```python
#coding=utf-8

from time import ctime,sleep

def timefun(func):
  def showtime():
    print ctime()
    return func()
  return showtime

@timefun
def foo():
  print "This is foo"

for i in range(3):
  foo()
  sleep(2)

print "-"*20
timefun(foo)

print "-"*20
timefun(foo)()
```

保存为decorator_improve.py，运行，看一下结果。                          
![decorator_improve.jpg](../../images/decorator_improve.jpg)                         

但是如果这样的话，就没有任何的区别了。                             

```python
#coding=utf-8

from time import ctime,sleep

def timefun(func):
  def showtime():
    print ctime()
    return func
  return showtime()

@timefun
def foo():
  print "This is foo"

for i in range(3):
  foo()
  sleep(2)

print "-"*20
timefun(foo)

print "-"*20
timefun(foo)()
```

保存为decorator_back.py，运行，看一下效果。                        
![decorator_back.jpg](../../images/decorator_back.jpg)             

装饰器也可以是一个类，使用`_call`函数，使在每次调用的时候使用装饰器即可。                  
现在就大概明白了，装饰器的功能就是在原有的函数功能的基础上包装一下，给它增加新的功能。
>或许有人会问，那为什么我们不去重写这个函数呢？
>1. 或许这个函数是标准函数库里的或者是他人写的函数，不好修改，我们只需给它加上一些装饰而已，就会比较简单。
>2. 或许我们并不是每一个函数都需要装饰，这样的话，更容易控制。            

装饰器用来做静态变量。                               

Python里是没有静态变量的，只有静态成员变量，但是我们有时候需要在函数里调用静态变量，可是又不想创建一个类，怎么办呢？                                    

首先是来看一下Python里面没有静态变量                            

```python
>>> def fin(x):
...     _i = 0
...     _i = _i+1
...     print _i
...     if x<2: return 1
...     return (fin(x-1)+fin(x-2))
...
>>> fin(5)
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
8
```

我们利用装饰器当做静态变量，但是非常坑爹的是，在非递归调用里可以正常使用，完全当做一个静态变量，但是在递归调用里就出问题。                        

```python
#coding=utf-8

def static(func):
  def count(*args):
    count._call += 1
    print count._call
    func(*args)
  count._call = 0
  return count

#在非递归调用中完全可以当做静态变量来使用
@static
def echo():
  pass

for i in range(5):
  echo()

#但是在递归调用中就出问题
# @decorator
# def fin(x):
#   if x<2: return 1
#   return (fin(x-1)+fin(x-2))

# print fin(5)
```

保存为static.py，运行，看一下结果。                               
![static.jpg](../../images/static.jpg)



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

######filter()

##对象内置函数

包括`__name__` `__call__` `__init__` `__name__`
