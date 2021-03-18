---
layout: post
description: Python 是如此的灵活，却也是这样的危险，一不小心，危机四伏。
title:  线上踩坑实录
category: blog
---


## 迭代器只能遍历一次

### 迭代器

迭代器只能循环一遍，在循环之后迭代器为空。

正常情况下不会用到迭代器，用到的时候需要小心。
同样的列表生成式，tuple 生成的就是迭代器，list 生成的还是列表
```
>>> [i for i in [1,2,3]]
[1, 2, 3]
>>> {i for i in [1,2,3]}
{1, 2, 3}
>>> (i for i in [1,2,3])
<generator object <genexpr> at 0x105bfd150>
```

迭代器，转化成 list 之后就为空，经过一次遍历就成空

```
>>> a = (i for i in [1,2,3])
>>> list(a)
[1, 2, 3]
>>> list(a)
[]
>>>
>>>
>>> b = (i for i in [1,2,3])
>>> [_ for _ in b]
[1, 2, 3]
>>> [_ for _ in b]
[]
```

### 线上问题

所以在双重列表生成式中，需要注意

```
>>> c = (i for i in [1,2,3])
>>> [i for i in [5,4,3] if i not in c]
[5, 4, 3]
```

这里的时间复杂度是 `O(m*n)`

会对迭代器做 m 次循环，但实际上只有第一次循环的时候迭代器中有值，剩下的 m-1 次循环都是空

> 竟然是和 insgram 遇到一样的问题 [Python向来以慢著称，为啥Instagram却唯独钟爱它？](https://www.infoq.cn/article/instagram-pycon-2017/)

## 整形类型转换

```
>>> int('12')
12
>>> int('12.0')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: invalid literal for int() with base 10: '12.0'
>>> int(float('12.0'))
12
```

int 整型不能强行转换浮点数

## 线程安全

一般在 python 中不会遇到线程安全问题，说明见过的世面还不够。

对于高并发的场景下，用`类变量`或者`单例的实例变量`，需要注意线程安全问题。

## 布尔运算

正数的布尔值为正，0 的布尔值为负，这很符合常识的吧，但是**负数的布尔值也为正**，😂。

```
>>> bool(1243)
True
>>> bool(45)
True
>>> bool(-45)
True
>>> bool(-0)
False
>>> bool(0)
False
>>> bool(-734251)
True
```

## 引用路径问题

有的时候，同一个对象的不同路径引用，其实是同一个对象。

```
In [140]: from marshmallow import missing as onemissing

In [141]: from marshmallow.utils import missing as twomissing

In [142]: onemissing
Out[142]: <marshmallow.missing>

In [143]: twomissing
Out[143]: <marshmallow.missing>

In [144]: onemissing is twomissing
Out[144]: True
```

但是有时候，同一个对象的不同路径引用方式，却是不同的对象。
> **这种情况一般发生在项目根目录和项目子目录都在 `PYTHONPATH` 中的时候，源自从项目根目录开始引用或者子目录开始引用的差异**

```
In [161]: from cherry.error import CustomException as ce

In [162]: from error import CustomException as ee

In [163]: ce
Out[163]: cherry.error.CustomException

In [164]: ee
Out[164]: error.CustomException

In [165]: ce is ee
Out[165]: False

In [166]: ce == ee
Out[166]: False

```

这里 `error.py` 是在 cherry 目录下，不过 cherry 的根目录和 cherry 子目录都在 `PYTHONPATH` 中。

`error.py` 文件内容。

```python
# -*- coding: utf-8 -*-
from socket import timeout


class CustomException(Exception):
    pass


```

但是从 error 中引用 timeout 其实都是 socket.timout ，即为同一个对象。

```
In [1]: import sys

In [2]: sys.path.insert(0, '/xx/yy/cherry')

In [3]: sys.path.insert(0, '/xx/yy')

In [4]: from cherry.error import timeout

In [5]: from cherry.error import timeout as ct

In [6]: from error import timeout as et

In [7]: ct
Out[7]: socket.timeout

In [9]: et
Out[9]: socket.timeout

In [10]: ct is et
Out[10]: True
```

这里其实使用 `type` 看一下对象类型就能发现差异或者使用 `id` 看下内存地址的差异，有的时候从不同路径引入的其实是同一个对象，但是有的时候是不同对象。

```
In [4]: from marshmallow import missing as onemissing

In [5]: from marshmallow.utils import missing as twomissing

In [6]: type(onemissing)
Out[6]: marshmallow.utils._Missing

In [7]: type(twomissing)
Out[7]: marshmallow.utils._Missing

In [8]: from cherry.error import CustomException as ce

In [9]: from error import CustomException as ee

In [10]: type(ce)
Out[10]: type

In [11]: type(ee)
Out[11]: type

In [12]: ce
Out[12]: cherry.error.CustomException

In [13]: ee
Out[13]: error.CustomException

In [14]: id(onemissing)
Out[14]: 140658795796368

In [15]: id(twomissing)
Out[15]: 140658795796368

In [16]: id(ce)
Out[16]: 140658767337664

In [17]: id(ee)
Out[17]: 140658759614048
```

## 序列化

非常低级的错误，json 不能序列化 set 集合，当多线程或其他无法及时查看到报错日志的时候，很难发现集合竟然不能被序列化。

```
>>> data = {"/asdsf"}
>>> import json
>>> json.dumps(data)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/bytedance/miniconda/envs/byted/lib/python2.7/json/__init__.py", line 244, in dumps
    return _default_encoder.encode(obj)
  File "/Users/bytedance/miniconda/envs/byted/lib/python2.7/json/encoder.py", line 207, in encode
    chunks = self.iterencode(o, _one_shot=True)
  File "/Users/bytedance/miniconda/envs/byted/lib/python2.7/json/encoder.py", line 270, in iterencode
    return _iterencode(o, 0)
  File "/Users/bytedance/miniconda/envs/byted/lib/python2.7/json/encoder.py", line 184, in default
    raise TypeError(repr(o) + " is not JSON serializable")
TypeError: set(['/asdsf']) is not JSON serializable
```
