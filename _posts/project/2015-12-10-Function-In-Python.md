---
layout: post
title: python的内置函数
category: project
description: 强大的Python不仅有面向对象的特性，而且有很多强大的内置函数。
---

Python的内置函数主要包括两大类，一是Python的函数式编程用到的函数，一是Python对象的内置函数。

## 函数式编程

#### 基本的内建函数

##### type判断对象类型

```python
>>> type(1)
<type 'int'>
>>> a = 1
>>> type(a)
<type 'int'>
>>> type("a")
<type 'str'>
>>> type([1,2])
<type 'list'>
>>> type((1,2))
<type 'tuple'>
>>> type({1,2})
<type 'set'>
>>> type({1:'one',2:'two'})
<type 'dict'>
>>> type(int)
<type 'type'>
>>> type(long)
<type 'type'>
>>> def my():
...     pass
...
>>> type(my)
<type 'function'>
>>> class my:
...     pass
...
>>> type(my)
<type 'classobj'>
>>> a = my()
>>> type(a)
<type 'instance'>
>>> class my(object):
...     pass
...
>>> type(my)
<type 'type'>
>>> a = my()
>>> type(a)
<class '__main__.my'>
>>> type(type)
<type 'type'>
```

>也可以用`__class__`

```python
>>> a = 1
>>> a.__class__
<type 'int'>
>>> a = "i"
>>> a.__class__
<type 'str'>
>>> def echo():
...     pass
...
>>> echo.__class__
<type 'function'>
>>> int.__class__
<type 'type'>
>>> type.__class__
<type 'type'>
>>> class foo:
...     def bar():
...             pass
...
>>> a = foo()
>>> a.__class__
<class __main__.foo at 0x0291EA40>
```

##### isinstance()判断变量

```python
>>> a = 1
>>> isinstance(a,int)
True
>>> isinstance(a,object)
True
>>> isinstance(a,type)
False
>>> isinstance(1,int)
True
>>> isinstance(1,object)
True
>>> isinstance(1,type)
False
>>> isinstance(1,str)
False
>>> isinstance("1",str)
True
>>> isinstance("1",object)
True
>>> isinstance(int,object)
True
>>> isinstance(int,type)
True
```

可以看到，在Python中其实也包含了万物皆对象的思想。

```python
>>> class foo:
...     name="foo"
...     def show():
...             print foo.name
...
>>> class bar:
...     name="bar"
...
>>> a = foo()
>>> isinstance(foo,object)
True
>>> isinstance(a,object)
True
>>> isinstance(a.show,object)
True
>>> isinstance(a,foo)
True
>>> isinstance(a,bar)
False
```

##### 对象类型转换

|函数                   |说明                                             |
|:-----:                |:------:                                         |
|int(x=0[,base=10])     |将其他进制的字符串或数转化为十进制整数，若为十进制浮点数，则表示取整|
|long(x=0[,base=10])    |将其他进制的字符串或数转化为长型数               | 
|float(x=0)             |将其他进制的字符串或数转化为浮点数               |
|round(x)               |将一个浮点数四舍五入进行取整                     |
|complex(real [,imag ]) |创建一个复数                                     |
|str()                  |将对象转换为对 用户 友好的字符串                 |
|repr()                 |将对象转换为对 Python 友好的字符串               |
|list()                 |将序列转换为列表                                 |
|bool()                 |将一个对象转换为布尔值                           |
|tuple()                |将序列转换为元组                                 |
|dict()                 |两个序列作为一个序列里的两个元素,将其转换为一个字典，或是将一些等式转换为字典           |
|set()                  |将序列转换为集合                                 |
|chr()                  |将一个整数转化为相应的ASCII字符                  |
|ord()                  |将一个ASCII字符转化为相应的整数                  |
|hex()                  |将一个整数转化为十六进制编码字符串               |
|oct()                  |将一个整数转化为八进制编码字符串                 |
|unicode(string[,encoding])                  |将其他格式的字符串转化为Unicode格式的字符串               |

##### 与数学有关的内置函数

- abs(x) 返回 x 的绝对值  
- coerce(x, y) 将 x,y 强制类型转换为两者中更精确的一种
- divmod() = ((x-x%y)/y, x%y) 返回商和余数
- round(number[, ndigits=1]) 四合五入，返回一个 ndigits 位的浮点数
- pow(x, y[, z]) = (x**y) % z 

#### id和del
查看变量位置和删除变量。
id()用来查看变量在内存中的位置，在深拷贝和浅拷贝的区别的时候就是通过查看在内存中的位置来判断的。
del 用来删除某个变量在内存中的占用。
Python是有自动的垃圾回收机制的，但是有时候我们想要显式的删除一个变量，就可以使用这个函数。

```python
>>> a = "a"
>>> a
'a'
>>> id(a)
39859168
>>> b = a
>>> b
'a'
>>> id(a)
39859168
>>> id(b)
39859168
>>> del a
>>> b
'a'
>>> id(b)
39859168
```

#### input和raw_input
input()相当于eval(raw_input())，input()和raw_input()都是标准输入函数。
raw_input()表示输入原生字符串，得到一个字符串，input()则是将其进行转换，故得到的可以是整形或浮点型输入。

```python
>>> a = raw_input("Please input a string: ")
Please input a string: This is a string
>>> a
'This is a string'
>>> type(a)
<type 'str'>
>>> b = raw_input()
12345
>>> b
'12345'
>>> type(b)
<type 'str'>
>>> a = input("Please input a string: ")
Please input a string: "This is a string"
>>> a
'This is a string'
>>> type(a)
<type 'str'>
>>> b = input()
12345
>>> b
12345
>>> type(b)
<type 'int'>
```

所以可以看到在input()里直接输入字符串时需要加上引号，如果不加直接写就会报错，而且可以在input()里面直接进行函数表达式。

```python
>>> a = input()
This is a string
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<string>", line 1
    This is a string
                   ^
SyntaxError: unexpected EOF while parsing
>>> a = input()
Thisisastring
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<string>", line 1, in <module>
NameError: name 'Thisisastring' is not defined
>>> a = input()
"Hello"+" "+"World"
>>> a
'Hello World'
>>> type(a)
<type 'str'>
>>> b = input()
100+200
>>> b
300
>>> type(b)
<type 'int'>
>>> b = input()
"100+200"
>>> b
'100+200'
>>> b = input()
"100"+"200"
>>> b
'100200'
```

#### Python的序列里支持函数表达。

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

#### Python函数支持不定长度的参数
用一个C语言里很经典的例子，求一个不定长度的数列的和。

```python
# coding=utf-8

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
![count.jpg](/images/count.jpg)

不仅仅是对列表类型的支持，字典也可以。

```python
# coding=utf-8

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
![count_dict.jpg](/images/count_dict.jpg)

#### Python 不再支持自加自减
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

#### python 没有三元运算符 ? :
如果学过其他的编程语言的话，三元运算符还是在很多地方很有帮助的，但是非常遗憾的是 python 并不支持原生的三元运算符，如果你需要这样的效果的话，可以用另一种方法。

其他编程语言：

```
a = 5 > 4 ? 1 : 2
```

python

```
a = 1 if 5 > 4 else 2
```

#### pyhton 跳出多重循环
单重循环还是和其他的编程语言一样的用单个 break 就可以了。

```python
i = 0
while 1:
    print i
    i += 1
    if i>5 :
        break
```

但是像这种的双层循环如果直接用两个 break 是无法跳出的，需要这样才能正常跳出循环。

```python
i = 0
while 1:
    print "Outer ",i
    while 1:
        print "Inner ",i
        if i>5:
            break
        i+=1
    else:
        continue
    break
```

结果是

```
Outer  0
Inner  0
Inner  1
Inner  2
Inner  3
Inner  4
Inner  5
Inner  6
```

#### range,zip,enumerate,all,any

###### range(start,stop[,step])
range()生成一个整数序列，一般用来计数。
主要有三种形式：
1. range(x)     表示生成从零开始到x的列表，一共有x个元素，所以不包括x。
2. range(x,y)   表示生成从x开始到y的列表，包含x不包含y。
3. range(x,y,z) 表示生成从x开始到y的间隔为z的列表，包含x不包含y。

```python
>>> range(10)
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> range(1,2)
[1]
>>> range(1,5)
[1, 2, 3, 4]
>>> range(1,10,2)
[1, 3, 5, 7, 9]
>>> range(0,10,2)
[0, 2, 4, 6, 8]
>>> m = 0
>>> for i in range(10):
...     m+=i
...
>>> m
45
```

>与x用法相同的还有一个'xrange'，用法完全一致，不过一个直接生成序列，一个生成可迭代的对象，在需要生成大数目的列表时，为了减少内存的消耗，推荐使用`xrange`来代替`range`。

###### zip(seq[,seq[,seq[...]]])
zip()函数，压缩，即将多个列表压缩为一个列表，如果列表长度不等，即以最短的那个为准。

```python
>>> zip([1,2,3])
[(1,), (2,), (3,)]
>>> zip([1,2,3],[4,5,6])
[(1, 4), (2, 5), (3, 6)]
>>> zip(range(1,5),range(3,9))
[(1, 3), (2, 4), (3, 5), (4, 6)]
>>> zip([1,2,3,4,5],["a","b","c","d"],(9,8,7))
[(1, 'a', 9), (2, 'b', 8), (3, 'c', 7)]
```

###### enumerate(seq,start=0)
enumerate()，将一个序列变成带下标的序列，相当于字典。`start`即初始计数位置。

```python
>>> a = ['one','two','three']
>>> i=0
>>> for each in a:
...     print "No %s is %s"%(i,each)
...     i+=1
...
No 0 is one
No 1 is two
No 2 is three
>>> for i,each in enumerate(a):
...     print "No %s is %s"%(i,each)
...
No 0 is one
No 1 is two
No 2 is three
>>> b = enumerate(a)
>>> b
<enumerate object at 0x029BDDC8>
>>> for i,j in b:
...     print i,j
...
0 one
1 two
2 three
>>> c = enumerate(a,3)
>>> for i,j in c:
...     print i,j
...
3 one
4 two
5 three
```

###### all(seq)
all()函数，当序列中的每一个值都为真时，返回真，只要有一个为假，即返回假。

```python
>>> all([1])
True
>>> all(["1","hello",0])
False
>>> all(["1","hellp",None])
False
>>> all(["10",123,"0"])
True
>>> all([False,123,"10",])
False
```

###### any(seq)
any()函数，当序列中只要有一个为真时，返回真。

```python
>>> any([1])
True
>>> any(["1","hellp",None])
True
>>> any([False,None,0])
False
>>> any([False,None,"0"])
True
```

#### help和__doc__
这两个是函数的内置函数，就是说每一个函数都会有这两个函数，实际上也可以用于函数库或者是类或者对象中。
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

#### dir和__dict__
这是用来查看函数或者对象的属性和方法的。
dir()返回列表，\_\_dict\_\_返回字典。
在新式类与旧式类的比较中会用到这些函数。

```python
>>> def foo():
...     pass
...
>>> type(foo)
<type 'function'>
>>> dir(foo)
['__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__doc__', '__format__', '__get__', '__getattribute__', '__globals__', '__hash__', '__init__', '__module__', '__name__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'func_closure', 'func_code', 'func_defaults', 'func_dict', 'func_doc', 'func_globals', 'func_name']
>>> foo.__dict__
{}
>>> class foo:
...     name="foo"
...     def bar():
...             print foo.name
...
>>> a = foo()
>>> type(foo)
<type 'classobj'>
>>> type(a)
<type 'instance'>
>>> dir(foo)
['__doc__', '__module__', 'bar', 'name']
>>> foo.__dict__
{'__module__': '__main__', 'bar': <function bar at 0x0265A330>, 'name': 'foo', '__doc__': None}
>>> dir(a)
['__doc__', '__module__', 'bar', 'name']
>>> a.__dict__
{}
>>> class foo(object):
...     name="foo"
...     def bar():
...             print foo.name
...
>>> a = foo()
>>> type(foo)
<type 'type'>
>>> type(a)
<class '__main__.foo'>
>>> dir(foo)
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'bar', 'name']
>>> foo.__dict__
dict_proxy({'__module__': '__main__', 'bar': <function bar at 0x02AE4C70>, 'name': 'foo', '__dict__': <attribute '__dict__' of 'foo' objects>, '__weakref__': <attribute '__weakref__' of 'foo' objects>, '__doc__': None})
>>> dir(a)
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'bar', 'name']
>>> a.__dict__
{}
```

#### 内嵌函数
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

#### 函数装饰器
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

![decorator_demo.jpg](/images/decorator_demo.jpg)

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

![decorator_improve.jpg](/images/decorator_improve.jpg)

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

![decorator_back.jpg](/images/decorator_back.jpg)

装饰器也可以是一个类，使用`__call__`函数，使在每次调用的时候使用装饰器即可。
现在就大概明白了，装饰器的功能就是在原有的函数功能的基础上包装一下，给它增加新的功能。
>或许有人会问，那为什么我们不去重写这个函数呢？
>1. 或许这个函数是标准函数库里的或者是他人写的函数，不好修改，我们只需给它加上一些装饰而已，就会比较简单。
>2. 或许我们并不是每一个函数都需要装饰，这样的话，更容易控制。

来试一个含参的装饰器

```
# coding=utf-8

from time import ctime,sleep

def showtime(func):
  def getnow(*args):
    """show the time when func run """
    print ctime()
    return func(*args)
  return getnow

@showtime
def greet(now):
  """ greet to others"""
  print "Good "+now

greet("Morning")

sleep(1)

greet("Afternon")

```

执行结果

```
Thu Oct 20 20:50:33 2016
Good Morning
Thu Oct 20 20:50:34 2016
Good Afternon
```

> 如果是含有多个参数，则使用 `*args, **kwargs` 来代替 `*args`

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
# @static
# def fin(x):
#   if x<2: return 1
#   return (fin(x-1)+fin(x-2))

# print fin(5)
```

保存为static.py，运行，看一下结果。

![static.jpg](/images/static.jpg)

#### 匿名函数

匿名函数的关键字是lambda，结构是` lambda [arg1[,arg2[,...]]] : expression `
匿名函数也可以有参数，甚至默认参数或者不定参数，也有函数表达式。只不过因为是匿名函数，所以需要在完成时即调用，或者将函数保存为变量，就可以通过调用变量来使用匿名函数。

一个简单的例子，a+b，b的默认值为 0 。

```python
>>> def add(a,b=0):
...     return a+b
...
>>> add(1,2)
3
>>> add(1)
1
>>> add = lambda a,b=0 : a+b
>>> add(1,2)
3
>>> add(1)
1
>>> (lambda a,b=0 : a+b)(1,2)
3
```

#### apply filter map reduce

###### apply(function,arges)
apply的功能是在不定长参数的函数中应用，在我们上面讲到不定长参数的使用时，传入一个序列或者字典时可以采用加`*`或者是`**`的形式，将序列传入函数，也可以采用apply。


用Python实现apply函数

```python
def apply(func,args):
  return func(*args)
```

其实不仅仅是不定长参数的函数，即使是在定长参数的函数中，如果需要多个参数也能使用。
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
![count_apply.jpg](/images/count_apply.jpg)

###### filter(func,seq)
fulter即过滤器，给定一个过滤函数和序列，每个序列元素都经过这个过滤函数删选，保留返回为真的元素。

用Python实现filter函数

```python
def filter(func,seq):
  filtered_seq = []
  for each in seq:
    if func(each):
      filtered_seq.append(each)
  return filtered_seq
```

例如我们现在随机产生10个100以内的整数，然后返回其中的所有奇数。

```python
#coding=utf-8

from random import randint

def odd(n):
  return n%2

allNum = []

for i in range(10):
  allNum.append(randint(1,99))

print filter(odd,allNum)
```

保存为create_odd.py，运行，看一下结果。
![create_odd.jpg](/images/create_odd.jpg)

可以看到每次结果都不一样，且返回不多于10个的奇数。

第一次重构

```python
#coding=utf-8

from random import randint

allNum = []

for i in range(10):
  allNum.append(randint(1,99))

print filter(lambda n : n%2 ,allNum)
```

保存为create_odd_lambda.py，运行，看一下结果。
![create_odd_lambda.jpg](/images/create_odd_lambda.jpg)

第二次重构

```python
#coding=utf-8

from random import randint

allNum = []

for i in range(10):
  allNum.append(randint(1,99))

print [n for n in allNum if n%2]
```

保存为create_odd_list.py，运行，看一下结果。
![create_odd_list.jpg](/images/create_odd_list.jpg)

第三次重构

```python
#coding=utf-8

from random import randint

print [n for n in [randint(1,99) for i in range(10)] if n%2]
```

保存为create_odd_list_list.py，运行，看一下结果。
![create_odd_list_list.jpg](/images/create_odd_list_list.jpg)

第四次重构

```python
#coding=utf-8

from random import randint

print filter(lambda x:x if x%2 else 0,[randint(1,99) for i in range(10)])

```

###### map(func,seq)
这个与apply()类似，也是将一个序列映射到函数上，不过这个不是将序列的值一次全部传入函数，而是将序列每个的值依次传入函数，然后将每次函数返回值组成序列返回。

用Python实现map函数

```python
def map(func,seq):
  mapped_seq = []
  for each in seq:
    mapped_seq.append(func(seq))
  return seq
```

小例子

```python
>>> map(lambda x:x**2,[1,2,3])
[1, 4, 9]
>>> map(lambda x:x+2 ,range(5))
[2, 3, 4, 5, 6]
```

其实，它不仅能够支持函数的一个参数输入，还能够多个参数输入。

```python
>>> map(lambda x,y:x+y ,[1,2,3],[4,5,6])
[5, 7, 9]
>>> map(lambda x,y:(x+y,x-y) ,[1,2,3],[4,5,6])
[(5, -3), (7, -3), (9, -3)]
>>> map(None ,[1,2,3],[4,5,6])
[(1, 4), (2, 5), (3, 6)]
```

###### reduce(func,seq,init=None)
这个函数的功能是把序列的第一个和第二个元素作为参数传入函数中，然后将得到的结果与第三个元素一起传入函数，然后将得到的结果与第四个元素一起传入函数。。。。一直到与最后一个元素一起传入函数，得到种的结果。
如果`init`不为`None`，则，一开始就是把`init`的值和第一个元素作为参数传入函数，然后一样的依次递归下去。

用Python实现reduce函数

```python
def reduce(func,seq,initial=None):
  Iseq = list(seq)
  if initial is None:
    res = Iseq.pop(0)
  else:
    res = init
  for each in Iseq:
    res = func(res,each)
  return res
```

小例子

```python
>>> reduce(lambda x,y:x+y ,range(5))
10
>>> reduce(lambda x,y:x+y ,range(5),10)
20
```

或者是使用 reduce 实现 lisp 风格的代码

```
# coding=utf-8

import operator

def f(op, *args):
  return {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.div,
    '&': operator.mod
  }[op](*args)

print f("*", f("+", 1, 2), 3)
```


#### yeild递推式

相当于一个生成器（generator），yield首先可以当做一般的return来使用，调用生成yield的函数返回的是一个yield实例，并没有数值，必须先执行next得到函数的第一个返回值，然后再次next，从上一个yield返回的地方继续执行得到第二个返回值，也就是说，在我们调用这个函数的时候函数其实并没有执行，只有在一次次的next中才一步步的执行了函数，最后整个函数执行结束，再执行next函数就会返回StopIteration异常。

```
>>> def foo():
...     for i in range(4):
...             yield i
...
>>> a = foo()
>>> a
<generator object foo at 0xb70692ac>
>>> a.next()
0
>>> a.next()
1
>>> a.next()
2
>>> a.next()
3
>>> a.next()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

#### exec，eval和execfile

eval：执行字符串中的**表达式**
exec：执行字符串中的**语句**
execfile：执行一个文件

##### eval
eval 是一个内建(buildin)函数，执行字符串中的表达式，返回值为表达式的值。不能执行语句，因为语句没有返回值。
input()相当于eval(raw_input())

```python
>>> eval("1+2")
3
>>> print eval("1+2")
3
>>> a
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'a' is not defined
>>> eval("a=1+2")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<string>", line 1
    a=1+2
     ^
SyntaxError: invalid syntax
>>> a = eval("1+2")
>>> a
3
>>> eval("1+2=")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<string>", line 1
    1+2=
       ^
SyntaxError: unexpected EOF while parsing
>>> eval("1+2=3")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<string>", line 1
    1+2=3
       ^
SyntaxError: invalid syntax
```
##### exec
exec 是一个语句，执行表达式中的语句，没有返回值。

```python
>>> exec("1+2")
>>> print exec("1+2")
  File "<stdin>", line 1
    print exec("1+2")
             ^
SyntaxError: invalid syntax
>>> b
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'b' is not defined
>>> exec("b=1+2")
>>> b
3
>>> exec("1+2=")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<string>", line 1
    1+2=
       ^
SyntaxError: invalid syntax
>>> exec("1+2=3")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<string>", line 1
SyntaxError: can't assign to operator

```

##### execfile
执行python脚本

#### 切片

python切片可以在字符串切片也可以给序列切片，用法`sequence[start,stop,step]`

```python
>>> a="abcdefg"
>>> a[-1:]
'g'
>>> a[:-1]                 //相当于字符串逆序
'abcdef'
>>> a[:]
'abcdefg'
>>> a[::-1]
'gfedcba'
>>> a[::-2]
'geca'
>>> a[2:-2]
'cde'
>>> b=["a","b","c","d","e"]
>>> b[::-1]
['e', 'd', 'c', 'b', 'a']
>>> b[1:-1]
['b', 'c', 'd']

```

python字符串逆序输出

```python
#coding=utf-8

a = "123456"

print a[::-1]

for i in range(len(a)-1,-1,-1):
    print a[i],

import sys

print ""

for i in range(len(a)-1,-1,-1):
    sys.stdout.write(a[i])

print ""
b = list(a)
b.reverse()
print "".join(b)

```

输出

```python
654321
6 5 4 3 2 1
654321
654321
```

#### 深拷贝与浅拷贝

在 python 中的对象赋值的时候，有时赋值并不是赋值，而是对象的地址，列表是直接赋值，但是列表中的列表的赋值就是地址，字典也是地址。

```
>>> a = [1,2]
>>> a
[1, 2]
>>> b = a
>>> b
[1, 2]
>>> b = [3,4]
>>> a
[1, 2]
>>> c = [[1,2],[3,4]]
>>> c
[[1, 2], [3, 4]]
>>> d = c
>>> c[0][0] = [3,4]
>>> c
[[[3, 4], 2], [3, 4]]
>>> d
[[[3, 4], 2], [3, 4]]
>>> e = {0:"00",1:"01"}
>>> f = e
>>> f[1] = "10"
>>> f
{0: '00', 1: '10'}
>>> e
{0: '00', 1: '10'}
```

这时，如果我们需要一个完全的直接赋值，可以使用 copy 这个函数库，它主要只有两个函数 copy() 和 deepcopy() 分别代表浅拷贝和深拷贝。

```
>>> c = [[1,2],[3,4]]
>>> d = copy.copy(c)
>>> d[0][0] = [3,4]
>>> d
[[[3, 4], 2], [3, 4]]
>>> c
[[[3, 4], 2], [3, 4]]
>>> c = [[1,2],[3,4]]
>>> d = copy.deepcopy(c)
>>> d[0][0] = [3,4]
>>> d
[[[3, 4], 2], [3, 4]]
>>> c
[[1, 2], [3, 4]]
>>> e = {0:"00",1:"01"}
>>> f = copy.copy(e)
>>> f[1] = "10"
>>> f
{0: '00', 1: '10'}
>>> e
{0: '00', 1: '01'}

```

还可以用 [:] 来达到 copy.copy 的效果

```
>>> a = [1,2,3,4]
>>> b = a[:]
>>> a
[1, 2, 3, 4]
>>> b
[1, 2, 3, 4]
>>> a.remove(1)
>>> a
[2, 3, 4]
>>> b
[1, 2, 3, 4]

```

#### 其他的常用函数

##### 字符串转大写，转小写，逆置

```
>>> a = "cbkBIKb3r45oinvs"
>>> a.upper()
'CBKBIKB3R45OINVS'
>>> a
'cbkBIKb3r45oinvs'
>>> a.lower()
'cbkbikb3r45oinvs'
>>> a[::-1]
'svnio54r3bKIBkbc'

```

##### 列表排序，逆置，最大值，求和，求频数，计数，去重

```
>>> b = [1,45,25,365,23,1,54,2]
>>> b.sort()
>>> b
[1, 1, 2, 23, 25, 45, 54, 365]
>>> a=reversed(b)
>>> a.next()
365
>>> a.next()
54
>>> a.next()
45
>>> a.next()
25
>>> b.reverse()
>>> b
[365, 54, 45, 25, 23, 2, 1, 1]
>>> max(b)
365
>>> sum(b)
516
>>> b.count(1)
2
>>> rates = {x:b.count(x) for x in set(b)}
>>> rates
{1: 2, 2: 1, 365: 1, 45: 1, 54: 1, 23: 1, 25: 1}
>>> set(b)
set([1, 2, 365, 45, 54, 23, 25])
```

##### 寻找当前文件夹下 root 文件夹中的最大文件

```
>>> import os
>>> print max([os.path.join(path,item) for path,_,items in os.walk(os.path.join(os.path.dirname(__file__),"root")) for item in items],key=lambda x:os.path.getsize(x))

```

功能同

```
find . -name "*.txt" -ls | sort -n -k7 | tail -n 1
```

##### 字典排序，倒置

```
>>> c = {1:12,4:15,9:242,4:25,1234:242,23:24}
>>> c
{1: 12, 1234: 242, 23: 24, 4: 25, 9: 242}
>>> sorted(c.iteritems(),key=lambda a:a[0],reverse=True) # 按键降序排列
[(1234, 242), (23, 24), (9, 242), (4, 25), (1, 12)]
>>> sorted(c.iteritems(),key=lambda a:a[0],reverse=False) # 按键升序排列
[(1, 12), (4, 25), (9, 242), (23, 24), (1234, 242)]
>>> sorted(c.iteritems(),key=lambda a:a[1],reverse=False) # 按值升序排列
[(1, 12), (23, 24), (4, 25), (1234, 242), (9, 242)]
>>> sorted(c.iteritems(),key=lambda a:a[1],reverse=True) # 按值降序排列
[(1234, 242), (9, 242), (4, 25), (23, 24), (1, 12)]
```

##### 字符串，列表转换

```
>>> b = [1,45,25,365,23,1,54,2]
>>> a = "Iwantyou"
>>> b = [x for x in a]
>>> b
['I', 'w', 'a', 'n', 't', 'y', 'o', 'u']
>>> "".join(b)
'Iwantyou'
>>> c = list(a)
>>> c
['I', 'w', 'a', 'n', 't', 'y', 'o', 'u']
```

##### 动态的往字典中添加键值对

可以使用 update 

```
>>> a={}
>>> a.update(title=12)
>>> a
{'title': 12}
```

##### partition

这是在 Python 2.5 中新加入的函数，其功能如下

```
>>> 'csdsdvdsds'.partition('ds')
('cs', 'ds', 'dvdsds')
```

相当于

```
>>> 'csdsdvdsds'[:'csdsdvdsds'.index('ds')]
'cs'
>>> 'csdsdvdsds'['csdsdvdsds'.index('ds')+len('ds'):]
'dvdsds'
```

还有从后往前查找函数 `rpartition`

## 对象内置函数

包括`__name__` `__call__` `__init__` `__main__` `__file__` `__exit__` `__enter__` `__getattr__` `__setattr__`  `__str__` `__new__` `__del__` `__repr__` `__all__`

有时间的时候还是要看一下

@classmethod @staticmethod @property __metaclass__

_XXX 私有类 __XXX 私有变量