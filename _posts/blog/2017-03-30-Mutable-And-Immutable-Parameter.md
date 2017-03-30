---
layout: post
title: python 中的可变参数和不可变参数
description: 数字，字符串和元组是不可变的，而列表，字典和对象都是可变的。
category: blog
---

可变对象和不可变对象的区别是即是他们的值是否可变，如字符串是不可变的，那么在你的每一次修改值的时候，其实你得到的已经不是之前的那个字符串对象了。

```
>>> a = 'origin is here'
>>> id(a)
8306144
>>> a = 'change it'
>>> a
'change it'
>>> id(a)
48359904
```

但是对不可变对象的复制是深复制，不过当对复制内容的修改时，就变成了浅复制，对复制内容的修改并不会体现在初始内容上。

```
>>> a = 'origin is here'
>>> b=a
>>> id(a)
44678624
>>> id(b)
44678624
>>> b = 'change it'
>>> a
'origin is here'
>>> id(a)
44678624
>>> id(b)
45935136
```

还有就是在函数调用的时候，对于不可变对象的引用并不是同一个，即形参与实参并不是指向同一个地址，在形参进行修改，并不会体现在实参上。

```
>>> def rename(n):
...     n='change it'
...
>>> a
'origin is here'
>>> rename(a)
>>> a
'origin is here'
```

而可变参数，形参和实参是一致的，在函数内对形参进行修改也会体现在实参上。

```
>>> def rename(n):
...     n[0]='change it'
...
>>> a = ['origin is here', ]
>>> rename(a)
>>> a
['change it']
```

对可变参数的复制也是深拷贝，对可变对象的修改即是对原对象的修改。

```
>>> a = ['origin is here', ]
>>> b=a
>>> id(a)
45947400
>>> id(b)
45947400
>>> b[0] = 'change it'
>>> a
['change it']
>>> b
['change it']
>>> id(a)
45947400
>>> id(b)
45947400
```

那么如果我们就是想要对可变对象的浅复制呢？可以使用 `copy ` 这个库，或者 列表也提供了一个浅复制的方法。

```
>>> a = ['origin is here', ]
>>> b=a[:]
>>> id(a)
45913672
>>> id(b)
45946200
>>> import copy
>>> c=copy.copy(a)
>>> id(c)
45999728
>>> b='change it'
>>> a
['origin is here']
>>> c='change it again'
>>> a
['origin is here']
```

同样的，`copy ` 这个库也提供了深拷贝，但是还是不能修改不可变对象。

```
>>> a='origin is here'
>>> b=copy.deepcopy(a)
>>> id(a)
45999632
>>> id(b)
45999632
>>> b='change it'
>>> a
'origin is here'
>>> id(a)
45999632
>>> id(b)
45935072
```