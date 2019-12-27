---
layout: post
title: Python 动态生成实例
description: 大家都知道 Python 是动态语言，动态语言的典型特征是什么呢？
category: blog
---

# 动态语言

Python 是一门典型的动态语言，一般来说的动态语言，值的其实是动态类型语言，就是在运行时才做类型校验和转换的，静态语言在编译时就做了类型校验，而且是强类型，不能随便转换。所以动态语言和静态语言也被称为 弱类型语言和强类型语言。

除了数据类型校验和转换之外，动态类型还能够 动态的添加或者修改和方法，实例，类和模块。虽然这个在静态类型语言，比如 Java 里用 ClassLoader 热更新也可以做，但是在 Python 里面可以更简单的实现。

最重要的是可以动态的执行代码，这一点简直无敌，比如 Python 的 eval .

## 方法和函数

方法包括类方法，静态方法和类方法的新增，修改，重写都可以，函数也是一样。

```
# coding=utf-8

code = """
def add(x, y):
    return x + y

"""

exec code
print 'dynastic add function add:', add(1, 2)

add = lambda x, y: x*y
print 'dynastic update function add:', add(1, 2)


class A(object):
    def __init__(self, source):
        self.source = source

    def add(self):
        return 0

a = A(1)
print 'source instance method add:', a.add()

A.add = lambda self, value: value + self.source
print 'dynastic update instance method add:', a.add(2)

A.div = classmethod(lambda cls, value: 1 / float(value))
print 'dynastic add class method div:', a.div(2)

A.min = staticmethod(lambda value: 1 - value)
print 'dynastic add static method min:', a.min(1)

a.mul = lambda x, y: x * y
print 'dynastic add instance static method mul:', a.mul(1, 2)


```


## 类和实例


```
# coding=utf-8


class A(object):
    pass


code = """
a = A()
"""
print 'dynastic create class:', A, A.__base__

exec code
print 'dynastic create A class instance:', a

a.name = "windard"
print 'dynastic update instance property:', a.name

b = type('B', (object,), {})
print 'dynastic create B class instance:', b

c = type('B', (type(b),), {"name": "windard"})
print 'dynastic create B class:', c, c.name

D = type(str(""), (A, ), {})
print 'dynastic create D class:', D, D.__base__

d = D()
print 'dynastic create D class instance:', d

E = type("E", (), {})
print 'dynastic E create class:', E, E.__base__

e = E()
print 'dynastic create E class instance:', e

# f = type("F", (e, ), {})
# print 'dynastic create e class instance:', f

G = type(str(""), (a.__class__, ), {})
print 'dynastic create G class:', G

g = G()
print 'dynastic create G class instance:', g


```

实例本身就是可以动态创建或者修改的，对实例的替换，其实就是对变量的替换，实例就会被垃圾回收。

动态创建类的核心在于使用 `type` 方法，这不就是可以用来判断类或者实例的 type，还能根据 type 生成其子类，比如 type 的实例是 class，class 的实例是 instance 。

type 的语法有两种

- type(object) 					查看一个 对象的父类，instance 父类 class，class 父类 type
- type(name, bases, dict)		创建一个 对象的实例，type 的实例 是 class，class 的实例是 instance 。
	参数
	name -- 类的名称。
	bases -- 基类的元组。基类为 class 则创建一个 instance，基类为 type 或者 空 则创建一个 class 。
	dict -- 字典，类内定义的命名空间变量。

## 包和模块

```
# coding=utf-8


def inner_function():
    from dynamic_class_and_instance import D
    d = D()
    print 'dynamic import module and create instance:', d


def import_function():
    module_meta = __import__('dynamic_class_and_instance')
    d = getattr(module_meta, 'D')()
    print 'dynamic import module and create instance:', d


def importlib_function():
    from importlib import import_module
    module_meta = import_module('dynamic_class_and_instance')
    d = getattr(module_meta, 'D')()
    print 'dynamic import module and create instance:', d


if __name__ == '__main__':
    # import_function()
    # inner_function()
    importlib_function()

```

动态引用包和模块很简单，主要需要其处在可引用的地方，比如在 `PYTHONPATH` 里，可以使用 `sys.path` 来动态更改 `PYTHONPATH` 路径来动态引用库。
