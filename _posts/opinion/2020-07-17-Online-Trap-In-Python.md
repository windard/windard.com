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

对于高并发的场景下，用类变量或者单例的实例变量，需要注意线程安全问题。
