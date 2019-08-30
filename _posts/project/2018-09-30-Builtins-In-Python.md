---
layout: post
title: python的内置函数
category: project
description: 真正的所有内置函数总结
---

这已经是第三篇关于 python 内置函数的文章了，前两篇都不成章法，想到多少写多少，这次比较成一条脉络。

本文执行环境 Mac python 2.7.

## 开始的开始

### globals

获得运行时所有的全局变量，比如在 shell 里时

```
>>> globals()
{'__builtins__': <module '__builtin__' (built-in)>, '__name__': '__main__', '__doc__': None, '__package__': None}
```

这里的 `__builtins__` 里就是我们所有的内置函数。

### locals

获得运行时的局部变量，在函数中即函数里的变量，在函数外相当于 `globals`

```
>>> def a():
...     b = 1
...     print globals()
...     print locals()
...
>>> a()
{'__builtins__': <module '__builtin__' (built-in)>, '__name__': '__main__', '__doc__': None, 'a': <function a at 0x10897ff50>, '__package__': None}
{'b': 1}
>>> globals()
{'__builtins__': <module '__builtin__' (built-in)>, '__name__': '__main__', '__doc__': None, 'a': <function a at 0x10897ff50>, '__package__': None}
>>> locals()
{'__builtins__': <module '__builtin__' (built-in)>, '__name__': '__main__', '__doc__': None, 'a': <function a at 0x10897ff50>, '__package__': None}
```

### vars

获得变量信息，无参数时相当于 `locals()`,有参数时即 `X.__dict__`

```
>>> vars()
{'__builtins__': <module '__builtin__' (built-in)>, '__name__': '__main__', '__doc__': None, 'a': <function a at 0x10897ff50>, '__package__': None}
>>> vars(a)
{}
>>> vars(vars)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: vars() argument must have __dict__ attribute
```

### __builtins__

`__builtins__` 其实也是一个 `module` , 即也是一个库，因为运行时即自动引入，无需手动引入，所以就叫做内建函数库。

函数库有 144 个函数或变量,上面提到的 `globals`, `locals`, `vars` 都在此列，算作内置函数。

> 不在此列还能直接使用的即为特殊关键字，比如说 `import`, `print`, `exec`, `del` <br>
> 关键字与内建函数的区别是内建函数可以给重新赋值，而关键字不能改变

```
>>> len(vars(__builtins__))
144
>>> __builtins__
<module '__builtin__' (built-in)>
>>> globals in  __builtins__.__dict__.values()
True
>>> vars in  __builtins__.__dict__.values()
True
>>> locals in  __builtins__.__dict__.values()
True
>>> import in  __builtins__.__dict__.values()
  File "<stdin>", line 1
    import in  __builtins__.__dict__.values()
            ^
SyntaxError: invalid syntax
>>> print in  __builtins__.__dict__.values()
  File "<stdin>", line 1
    print in  __builtins__.__dict__.values()
           ^
SyntaxError: invalid syntax
```

所以我们所称为内建函数，内置函数之类的都是指的在 `__builtins__` 库中的方法函数。

可以大概分为以下几类
- 特殊方法
- 内置函数
- 内置类型
- 内置变量
- 内置异常
- 内置错误
- 内置警告
- 证书版权

## 特殊方法

- `__doc__`
- `__import__`
- `__name__`
- `__package__`
- `__debug__`

### `__doc__`

返回类的说明文档，无主体的话即表示 `None`

```
>>> __doc__
>>> __builtins__.__doc__
"Built-in functions, exceptions, and other objects.\n\nNoteworthy: None is the `nil' object; Ellipsis represents `...' in slices."
>>> print vars.__doc__
vars([object]) -> dictionary

Without arguments, equivalent to locals().
With an argument, equivalent to object.__dict__.
```

### `__import__`

相当于 `import` ，将一个关键字改成一个内置方法,用来动态加载类和函数。

```
>>> __import__('json')
<module 'json' from '/Users/windard/anaconda/envs/python27/lib/python2.7/json/__init__.pyc'>
```

### `__name__`

类，库，示例，函数名。无主体时即当前进程名。

```
>>> __builtins__.__name__
'__builtin__'
>>> __name__
'__main__'

```

在文件中有一个 `__file__` 特殊方法，表示文件名或文件所在库名。

### `__package__`

包名,无主体时返回 None

```
>>> import json
>>> __builtins__.__package__
>>> json.__package__
'json'
>>> json.__name__
'json'
```

### `__debug__`

是否为 debug 模式

```
>>> __debug__
True
>>> __builtins__.__debug__
True
>>> json.__debug__
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'module' object has no attribute '__debug__'
```

## 内置函数

- globals
- locals
- vars

- all
- any
- filter
- reduce
- apply
- map
- zip

- sum
- len
- max
- min

- bin
- oct
- hex
- chr
- ord
- unichr

- isinstance
- issubclass
- callable

- format
- repr
- sorted
- reversed
- iter
- next
- reload

- round
- abs
- hash
- cmp
- intern
- coerce
- dir
- range
- pow
- divmod

- quit
- exit
- help
- print

- getattr
- hasattr
- delattr
- setattr

- execfile
- eval
- compile

- id
- open
- input
- raw_input


### unichr

同 chr 将数字转换为字符串，其转为 Unicode

```
>>> chr(56)
'8'
>>> chr(78)
'N'
>>> unichr(56)
u'8'
>>> unichr(78)
u'N'
```

### issubclass

判断一个类是否为另一个类的子类

```
>>> isinstance(1, int)
True
>>> isinstance(1, object)
True
>>> isinstance(1, type)
False
>>> issubclass(int, type)
False
>>> issubclass(int, object)
True
>>> isinstance(int, type)
True
>>> isinstance(object, type)
True
>>> isinstance(type, object)
True
>>> issubclass(object, type)
False
>>> issubclass(type, object)
True
```

### format

`format` 做函数使用表示将变量按照给定格式进行格式化，做方法使用表示格式化字符串

```
>>> format(11, '#X')
'0XB'
>>> format(11, '2%')
'1100.000000%'
>>> format(11, '#x')
'0xb'
>>> format(11, '#o')
'0o13'
>>> format(38, '08b')
'00100110'
>>> format(38, 'b')
'100110'
>>> format(38, 'd')
'38'
>>> 'hello {}'.format('world')
'hello world'
>>> 'hello {}'.format('windard!')
'hello windard!'
>>>
```

format 默认使用 `str` 如果需要展示特殊字符，使用 `!r` 表示 `repr` 格式化展示输出

```
>>> print "{}".format(b'\x01\x02')

>>> '{}'.format('\x01\x02')
'\x01\x02'
>>> print "{!r}".format(b'\x01\x02')
'\x01\x02'
```

## iter

迭代器函数,可以将一个序列转换为迭代器

```
>>> iter([1,2,3])
<listiterator object at 0x108abddd0>
>>> list(iter([1,2,3]))
[1, 2, 3]
```

也可以用来做一个 for 的死循环

```
>>> for i in iter(int, 1):
...     print 1
```

### compile

将一个字符串编译为字节代码,使用 `eval` 执行。

```
>>> c = compile('1+1', '', 'eval')
>>> c
<code object <module> at 0x10894d630, file "", line 1>
>>> eval(c)
2
```

### repr

`repr` 仅仅只是方法，而 `str` 既是方法，也是类型。

### print

print 很特殊，它既是一个关键字，也是一个内置方法。做 python 2 的写法是 关键字，做 python 3 的写法是 特殊方法。所以在 python 3 中将其关键字给剔除掉了。

```
>>> print 1
1
>>> print(1)
1
>>> print (1)
1
```

### exit

没想到吧，`exit` 也是函数，所以直接 `exit` 无法直接退出，`quit` 同理。

### dir

获得类的键，相当于 `X.__dict__.keys()`，如果无主体的调用相当于 `globals().keys()`

```
>>> len(dir(__builtins__))
144
>>> globals().keys()
['a', 'c', 'b', '__builtins__', 'value', '__package__', 'i', 'json', 'abs', 'exit', 'key', '__name__', 'foo', '__doc__']
>>> dir()
['__builtins__', '__doc__', '__name__', '__package__', 'a', 'abs', 'b', 'c', 'exit', 'foo', 'i', 'json', 'key', 'value']
```

### divmod

### intern

字符串驻留机制。对同一个字符串指向同一个地址,节约内存使用,提高代码效率。

python 对常用小整数和字符串有一个常量池保存，也可以使用 `intern` 来让变量强行保存下来。

小整数的范围是 `[-5, 256]`

```
>>> a = -5
>>> b = -5
>>> a is b
True
>>> a = -6
>>> b = -6
>>> a is b
False
>>> a = 256
>>> b = 256
>>> a is b
True
>>> a = 257
>>> b = 257
>>> a is b
False
```

字符串的常量规则是长度小于20，无空格标点特殊字符的为保存在常量池。

```
>>> a = 'a'*20
>>> b = 'a'*20
>>> a is b
True
>>> a = 'a'*21
>>> b = 'a'*21
>>> a is b
False
>>> a = "hello world"
>>> b = "hello world"
>>> a is b
False
>>> a = "helloworld"
>>> b = "helloworld"
>>> a is b
True
```

使用 intern 保存字符串常量

```
>>> a = intern('a'*21)
>>> b = intern('a'*21)
>>> a is b
True
>>> a = intern('hello world')
>>> b = intern('hello world')
>>> a is b
True
```

尝试的伪代码实现

```
reserved = []
def intern(s):
    if s in reversed:
        return s
    else:
        s = String()
        reversed.append(s)
        return s
```

实际的伪代码实现

```
interned = None

def intern(string):
    if string is None or not type(string) is str:
        raise TypeError

    if string.is_interned:
        return string

    if interned is None:
        global interned
        interned = {}

    t = interned.get(string)
    if t is not None:
        return t

    interned[string] = string
    string.is_interned = True
    return string
```

再测试了一下，在行内和定义变量也不一样

```
>>> "hell o" is "hell o"
True
>>> s1="hell o"
>>> s2="hell o"
>>> s1 is s2
False
>>> 'a'*20 is 'a'*20
True
>>> 'a'*21 is 'a'*21
False
```

### coerce

将两个变量转为同一种类型

```
>>> coerce(10, 10.12)
(10.0, 10.12)
```

## 内置类型

- bool
- int
- float
- long
- complex
- list
- tuple
- slice
- dict
- set
- frozenset
- basestring
- str
- bytes
- unicode
- bytearray
- memoryview
- enumerate
- xrange
- buffer
- file
- super
- type
- object
- property
- classmethod
- staticmethod

### bool

布尔类型，有且仅有两个内置变量 `True` 和 `False`

### unicode

Unicode 字符串，在 python 2 中 `str` = `bytes` ，在 python 3 中 `str` == `unicode`

### bytearray

字节数组.使用方式
- 如果 source 为整数，则返回一个长度为 source 的初始化数组；
- 如果 source 为字符串，则按照指定的 encoding 将字符串转换为字节序列；
- 如果 source 为可迭代类型，则元素必须为[0 ,255] 中的整数；
- 如果 source 为与 buffer 接口一致的对象，则此对象也可以被用于初始化 bytearray。
- 如果没有输入任何参数，默认就是初始化数组为0个元素。

```
>>> bytearray()
bytearray(b'')
>>> bytearray(10)
bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
>>> bytearray('asds')
bytearray(b'asds')
>>> bytearray(iter([1,2,6,56,3,23]))
bytearray(b'\x01\x02\x068\x03\x17')
>>> 'helloworld'.encode('hex')
'68656c6c6f776f726c64'
>>> bytearray.fromhex('68656c6c6f776f726c64')
bytearray(b'helloworld')
```

### property

属性方法，一般在类中使用，使用方式 `@property` ，表示这是一个属性

### classmethod

类方法，一般在类中使用，使用方式 `@classmethod` ， 表示这是一个类方法

### staticmethod

静态方法，一般在类中使用，使用方式 `@staticmethod`，表示这是一个类静态方法

## 内置常量

- True
- False
- None
- Ellipsis
- _
- NotImplemented

### Ellipsis

省略号，在 python 2 中无明显意义。

```
>>> a = [1,2]
>>> a.append(a)
>>> a
[1, 2, [...]]
>>> bool(Ellipsis)
True
>>> type(Ellipsis)
<type 'ellipsis'>
>>> Ellipsis.__doc__
```

在 python 3 中

```
>>> ...
Ellipsis
>>> def foo():
...     ...
...
```

### _

`_` 可以作为变量名，其实它已经是一个常量，`__builtins__` 中本来只有143个变量，在执行过任何结果之后，`_` 就被赋值为上一个操作的结果。

```
>>> len(__builtins__.__dict__.keys())
143
>>> len(__builtins__.__dict__.keys())
144
>>> _
144
>>> 1+1
2
>>> _
2
>>> a = 3
>>> _
2
```

### NotImplemented

这是一个`未定义`的常量,可以用来取代 `NotImplementedError` ，因为有的地方你并不想 `raise NotImplementedError` 而且需要 `return NotImplemented` ，这样在未定义的时候也不会抛出异常。

```
>>> NotImplemented
NotImplemented
>>> type(NotImplemented)
<type 'NotImplementedType'>
>>> raise NotImplemented()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'NotImplementedType' object is not callable
>>> NotImplemented.__doc__
>>> bool(NotImplemented)
True
```

## 内置异常


- Exception
- BaseException
- StopIteration
- SystemExit
- GeneratorExit
- KeyboardInterrupt


## 内置错误

- IOError
- OSError
- EOFError
- TabError
- KeyError
- IndexError
- SyntaxError
- NameError
- StandardError
- BufferError
- FloatingPointError
- ReferenceError
- TypeError
- SystemError
- RuntimeError
- MemoryError
- LookupError
- ImportError
- ValueError
- UnicodeError
- UnicodeDecodeError
- UnicodeEncodeError
- UnicodeTranslateError
- ArithmeticError
- EnvironmentError
- ZeroDivisionError
- IndentationError
- AssertionError
- UnboundLocalError
- NotImplementedError
- AttributeError
- OverflowError

## 内置警告

- BytesWarning
- RuntimeWarning
- Warning
- FutureWarning
- ImportWarning
- UserWarning
- UnicodeWarning
- DeprecationWarning
- SyntaxWarning
- PendingDeprecationWarning

## 证书版权

- copyright
- credits
- license

### copyright

python 版权

```
>>> copyright
Copyright (c) 2001-2016 Python Software Foundation.
All Rights Reserved.

Copyright (c) 2000 BeOpen.com.
All Rights Reserved.

Copyright (c) 1995-2001 Corporation for National Research Initiatives.
All Rights Reserved.

Copyright (c) 1991-1995 Stichting Mathematisch Centrum, Amsterdam.
All Rights Reserved.
```

### credits

python 支持

```
>>> credits
    Thanks to CWI, CNRI, BeOpen.com, Zope Corporation and a cast of thousands
    for supporting Python development.  See www.python.org for more information.
```

### license

python 证书

```
>>> license
Type license() to see the full license text
>>> license()
A. HISTORY OF THE SOFTWARE
==========================

Python was created in the early 1990s by Guido van Rossum at Stichting
Mathematisch Centrum (CWI, see http://www.cwi.nl) in the Netherlands
as a successor of a language called ABC.  Guido remains Python's
principal author, although it includes many contributions from others.

In 1995, Guido continued his work on Python at the Corporation for
National Research Initiatives (CNRI, see http://www.cnri.reston.va.us)
in Reston, Virginia where he released several versions of the
software.

In May 2000, Guido and the Python core development team moved to
BeOpen.com to form the BeOpen PythonLabs team.  In October of the same
year, the PythonLabs team moved to Digital Creations (now Zope
Corporation, see http://www.zope.com).  In 2001, the Python Software
Foundation (PSF, see http://www.python.org/psf/) was formed, a
non-profit organization created specifically to own Python-related
Intellectual Property.  Zope Corporation is a sponsoring member of
the PSF.
```

## 参考链接

[你所不知道的 Python 冷知识](https://juejin.im/post/5b8d4f7651882542d14dab2b)

[bytearray](https://python-reference.readthedocs.io/en/latest/docs/functions/bytearray.html)

[python string intern](https://michaelyou.github.io/2016/07/10/python-string-intern/)
