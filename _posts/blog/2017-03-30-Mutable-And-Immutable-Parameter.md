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

最后，我们来深入研究一下它们之间的区别，我们就以数字，字符串，列表，元组，字典这六种类型为例探讨一下。

先来看一下它们实例所属的类和父类

```
# print 1.__base__                          # SyntaxError
# print 'a'.__base__                        # AttributeError
# print [].__base__                         # AttributeError
# print ().__base__                         # AttributeError
# print {}.__base__                         # AttributeError  
# print 1.__class__                         # SyntaxError
type(1) 									# <type 'int'>
print 'a'.__class__                         # <type 'str'>
print [].__class__                          # <type 'list'>
print ().__class__                          # <type 'tuple'>
print {}.__class__                          # <type 'dict'>
```

为什么会这样，所有的实例都没有父类，或语法错误，或属性错误，但是它们都还是属于它们原始的那个类型，int 类型最为特殊，不能用 `__class__` 查看所属类型，不过可以使用 `type` 查看其类型。

那么我们查看它们所在类型的父类和所属类。

```
print int.__base__                          # <type 'object'>
print str.__base__                          # <type 'basestring'>
print str.__base__.__base__                 # <type 'object'>
print list.__base__                         # <type 'object'>
print set.__base__                          # <type 'object'>
print dict.__base__                         # <type 'object'>
print int.__class__                         # <type 'type'>
print str.__class__                         # <type 'type'>
print set.__class__                         # <type 'type'>
print list.__class__                        # <type 'type'>
print dict.__class__                        # <type 'type'>
```

虽然 str 的直接父类并不是 object ，不过它的最终父类还是 object ，所以也就是所有的类型的最终父类都是对象，即 一切皆对象， 或者 一切都是对象的子类。

但是为什么所有的类型的当前类是 type ，type 是什么？

```
print isinstance(1, object)                   # True
print isinstance('a', object)                 # True
print isinstance([], object)                  # True
print isinstance((), object)                  # True
print isinstance({}, object)                  # True
print isinstance(int, object)                 # True
print isinstance(str, object)                 # True
print isinstance(list, object)                # True
print isinstance(set, object)                 # True
print isinstance(dict, object)                # True
print isinstance(type, object)                # True
```

不管你现在是个什么玩意儿，都是 object 的实例，你的类都是直接或间接继承自 object。

但是还是不太明白 type 是什么， type 到底是从何处来，为什么在查看所有的类型的时候，它的类型都是 `<type XXX>` 。

看一下  type 的父类和类

```
print type.__base__                         # <type 'object'>
print type.__class__                        # <type 'type'>
```

type 的父类是 object ，现在的类就是 type ，它也是继承自 object ，但是它和 object 到底是什么关系呢？

type 和 object 的关系与 可变对象和不可变的关系 有联系么？

暂时还不是很清楚，关于 type 和 object 的关系可以参看[这篇文章](https://windard.com/project/2016/11/07/Function-In-Python-Class)。
