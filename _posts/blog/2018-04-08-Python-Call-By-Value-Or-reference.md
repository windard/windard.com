---
layout: post
title: python 函数调用是值传递还是引用传递
description: Neither of them, call by object
category: blog
---

## python 数据类型

python 中的基本数据类型有六种：数字，字符串，列表，字典，元组和集合，(Number, String, List, Dict, Tuple, Set)
 - 数字包括整形，长整型，浮点型和复数，(Int, Long, Float, Complex)
 - 布尔值 True 和 False
 - 集合包含集合和不可变集合 (set, frozenset)
 - 字符串里包括 字符串，字节串和万国码 (str, bytes, unicode)
 - 列表包括 列表和字节数组 (list, bytearray)
 - 有的时候分四种，就是数字，序列，集合和字典。序列里包括字符串和列表和元组。
 - 有的时候分五种，就是数字，字符串，列表，元组和字典。列表里包括元组。

其中不可变的类型有数字，字符串，布尔值，元组，和 frozenset， 可变类型有列表，字典，和集合。

可变和不可变的区分是该对象是否存在 add 或者 append 等方法来增加对象元素，使得对象在不改变自身 ID 的情况改变内容。

像数字和字符串对象是不可变的，但是数字和字符串变量可以随意赋值，因为在赋值的同时，并没有修改原始对象本身，而是新生成了一个对象赋值给原始变量。

    ```
    h = 1
    print h, id(h)
    # 1 140726637739528
    h = 2
    print h, id(h)
    # 2 140726637739504

    i = '1'
    print i, id(i)
    # 1 4414452640
    i = '2'
    print i, id(i)
    # 2 4415066400
    ```

> 在字符串操作中，字符串不能被改变，表示字符串中的元素不能被重新赋值，比如 `i[0] = '2'` 就会报错。

像列表，字典对象是可变的，即可以增加删减元素，而对象本身 ID 和变量值不变，但是当可变变量被重新赋值的时候，其对象 ID 是改变的。

    ```
    f = [1, 2]
    print f, id(f)
    # [1, 2] 4452026200
    f.append(3)
    print f, id(f)
    # [1, 2, 3] 4452026200
    f = [3]
    print f, id(f)
    # [3] 4452026272

    g = {}
    print g, id(g)
    # {} 4449336408
    g['name'] = 'windard'
    print g, id(g)
    # {'name': 'windard'} 4449336408
    ```

> 在比较两个对象值是否相等的时候，用 `=` 即可，在判断两个对象 ID 是否相等的时候，用 `is`

不可变对象之所以不可变，是因为其没有内部元素，或者内部元素不能重新赋值，或者对象大小固定。

可变对象之所以可变，因为对象大小不固定，或者可以给内部元素重新赋值，所以在修改内部元素的时候，整个对象没有改变。如果对可变对象重新赋值，那可变对象的 ID 也会改变。

所以不可变对象也不一定是绝对的不可变，比如

```
>>> a = ([], [])
>>> id(a)
4478559512
>>> a
([], [])
>>> a[0].append(1)
>>> id(a)
4478559512
>>> a
([1], [])
```

或者 `+=` 与 `=+` 的区别，前者是保持对象不变的增加，后者是创建新的对象，但是测试中对字符串和列表的使用不一致，在 python 与 ipython 中也不一致，有点迷。

## 一切皆对象

> Everything in Python is an object

在 python 中，一切皆对象，包括数字和字符串。

在可变与不可变的讨论中，一切的基础都是数字和字符串，他们是不可变的。

所以在变量与变量赋值的时候，都是浅拷贝，即其实是都将对象传递变量。

浅拷贝的意思是改变新变量，如果是不可变对象，原始变量值不变，如果是可变对象，原始变量的值随之改变。

根据可变对象和不可变对象的判别，本来就应该是这样的。

因为对于不可变对象，改变不可变对象，即是对变量的重新赋值，所以对原始变量无影响。对于可变对象，改变可变对象，即是对对象的元素进行操作，本来就是会影响到原始变量的。如果对新变量进行重新赋值，即可看到对原始变量不影响。

## python 中的函数传递

函数传递和变量赋值是一样的，有人以为是值传递，因为对原始变量无影响。但是没有看到函数传递的本质，ID 不变，改变即重新赋值。

> 值传递是值在调用函数时，将实际参数复制一份传递到函数中，这样在函数中如果对参数进行修改，将不会影响到实际参数。

```
# coding=utf-8

def value_delivery():
    a = 1
    print 'source', a, id(a)
    change_value(a)
    print 'after', a, id(a)


def change_value(a):
    print a, id(a)
    a = 2
    print a, id(a)


if __name__ == '__main__':
    value_delivery()

```

可以看到说的是值传递，其实是对象传递

```
source 1 140587012477912
1 140587012477912
2 140587012477888
after 1 140587012477912
```

有人说是引用传递，因为函数中修改影响了原始变量。但是没有看到在函数中只是对变量的元素进行修改，而不是对变量的重新赋值。如果真的是引用参数，对变量的重新赋值也是会改变原始变量。

> 引用传递是值在调用函数时，将实际参数的地址传递到参数中，那么在函数中对参数所进行的修改，将影响到实际参数。

```
# coding=utf-8


class User():
    def __init__(self, name, year):
        self.name = name
        self.year = year

    def __str__(self):
        return '<User %s:%s>' % (self.name, self.year)


class Man():
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def __str__(self):
        return '<Man %s:%s>' % (self.name, self.phone)


def quote_delivery():
    a = User('windard', 23)
    print 'source', a, id(a)
    change_quote(a)
    print 'after', a, id(a)


def change_quote(a):
    print a, id(a)
    a.name = 'other'
    print a, id(a)


if __name__ == '__main__':
    quote_delivery()
```

可以看到说是引用传递，其实是对象传递

```
source <User windard:23> 4347008064
<User windard:23> 4347008064
<User other:23> 4347008064
after <User other:23> 4347008064
```

如果对传入参数进行重新赋值，就不会修改到原始变量

```
# coding=utf-8


class User():
    def __init__(self, name, year):
        self.name = name
        self.year = year

    def __str__(self):
        return '<User %s:%s>' % (self.name, self.year)


class Man():
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def __str__(self):
        return '<Man %s:%s>' % (self.name, self.phone)


def quote_exchange():
    a = User('windard', 23)
    print 'source', a, id(a)
    quote_to_string(a)
    print 'after', a, id(a)


def quote_to_string(a):
    print a, id(a)
    a = "windard yang"
    print a, id(a)


if __name__ == '__main__':
    quote_exchange()
```

看到对象传递的实质

```
source <User windard:23> 4575444792
<User windard:23> 4575444792
windard yang 4575531224
after <User windard:23> 4575444792
```

在 Java 中，也是一切皆对象。这也就意味着，函数传递和变量赋值是和 python 一样的道理。