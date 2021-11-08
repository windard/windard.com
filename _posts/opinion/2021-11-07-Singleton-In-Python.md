---
layout: post
title: Python 中的单例模式
description: 一般在 Java 中的 单例模式出现的会比较多，Python 中其实也有
category: opinion
---

## 引子

在 Java 面试的八股文中，经常会被问到设计模式，各种设计模式中就有一种单例模式，就是在讲如何创建一个全局唯一的对象。

在 Python 中的设计模式讲的比较少，我一开始也没有听懂这个问题。

在 Python 的初始化的对象本来不就是唯一的么，在任意一个文件中初始化这个类生成对象，然后在其他地方引用不就可以了么？

后来见得多了才明白，原来问题是说 如何多次初始化一个类，生成的都是同一个对象，拿到的都是同一个对象引用。

这就有点意思了。

## 对象生成和初始化

我们都知道在 Python 中的实例方法 `__init__`,可以进行对象初始化赋值。

但是这个方法只是在进行初始化赋值，即使没有初始化业能够生成对象，这说明初始化之前对象就已经被创建出来了，被分配到了内存空间。

这就涉及到 Python 中的另一个魔术方法 `__new__` 用来生成对象。

实际是在 new 方法中生成对象，然后在实例方法中进行对象初始化，如果 new 方法没有返回对象，那么 init 方法也没有办法初始化。

new 和 init 的区别在于 new 是生成函数，必须有返回值，返回值就是实例对象，init 是初始化函数，用来定义实例属性，只有赋值语句，不能有返回值。

```
                   +------+
                   |  类  |
                   +------+
                      |
                      v
            +--------------------+
            |      __new__       |
            |  为对象分配内存空间  |
            |  返回对象地址引用    |
            +--------------------+
                      |
                      v
            +--------------------+
            |      __init__      |
            |      对象初始化     |
            |     定义实例属性     |
            +--------------------+
                      |
                      v
               +------------+
               |  实例对象   |
               +------------+

```

简单的例子

```python
# -*- coding: utf-8 -*-

class EmptyClass(object):
    def __new__(cls, *args, **kwargs):
        # 对象的创建参数就是 实例化时传入的参数
        print("__new__ is called")
        # 如果去掉下面一行，那么实例方法也不会被调用，类实例化得到的对象就是一个 None
        # return super(EmptyClass, cls).__new__(cls, *args, **kwargs)

    def __init__(self):
        print("__init__ is called")


if __name__ == '__main__':
    e = EmptyClass()
    print(e)

```

## 单例模式

我们已经知道在 `__new__` 方法中可以决定生成的对象实例，那么我们只需要控制 new 方法都返回同一个对象不就可以了？

```python
# -*- coding: utf-8 -*-


class OneInstance(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            # 使用继承的父类方法，或者直接使用对象的生成方法都可以
            # cls._instance = super(OneInstance, cls).__new__(cls, *args, **kwargs)
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, name):
        self.name = name

if __name__ == '__main__':
    o = OneInstance("o")
    b = OneInstance("b")
    print(id(o))
    print(id(b))
    print(o.name)
    print(b.name)

```

结果可以看到，我们确实每次实例化拿到都是同一个对象，在同一个内存地址，而且每次实例化都是在操作同一个对象。

```
140429306328016
140429306328016
b
b
```

这是最简单的单例模式，比较类似于 Java 中的懒汉模式，没有双重校验，因为 Python 中的 GIL 没有进程竞争问题。

但是它也不是线程安全的，如果需要线程安全的话，可能还需要一些其他的校验保障。

然后有一个地方需要注意，对于单例类和单例类的子类，因为这个类的实例化对象其实是挂在类上的静态属性。

如果先实例化单例类，在实例化单例类的子类，得到都是同一个对象实例，即父级单例类的实例对象，而且在实例化子类的时候，不会调用子类的实例方法。

如果先实例化单例类的子类，再实例化单例类，就会得到两个对象实例，分别是单例类的对象实例和子类的对象实例。

```python
# -*- coding: utf-8 -*-


class OneInstance(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            # cls._instance = super(OneInstance, cls).__new__(cls, *args, **kwargs)
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, name):
        self.name = name


class SubOneInstance(OneInstance):
    def __init__(self, name):
        super(SubOneInstance, self).__init__(name)
        self.family = "singleton"

    def print(self):
        return self.family


if __name__ == '__main__':

    s = SubOneInstance("s")
    p = SubOneInstance("p")
    o = OneInstance("o")
    b = OneInstance("b")
    print(id(o))
    print(id(b))
    print(id(s))
    print(id(p))
    print(o.name)
    print(b.name)
    print(s.name)
    print(p.name)
    print(o)
    print(b)
    print(s)
    print(p)
    print(p.family)
    print(s.print())

```

得到的是两个对象实例

``` 
140336958240656
140336958240656
140336958239696
140336958239696
b
b
p
p
<__main__.OneInstance object at 0x7fa2be8b7790>
<__main__.OneInstance object at 0x7fa2be8b7790>
<__main__.SubOneInstance object at 0x7fa2be8b73d0>
<__main__.SubOneInstance object at 0x7fa2be8b73d0>
singleton
singleton
```

## 子类的单例模式

上面提到的单例模式，都是针对于某一个特定的类，如果我们想某些类都是单例模式，生成的实例对象都是单个的，这应该如何处理呢？

### 元类编程

总不能把 `__new__` 方法在每个类定义上都抄一遍吧，如果使用子类继承的话，那么如果先实例化了父类，那么每个子类都是使用同一个父类实例对象，这样也不行。

既然 `__new__` 方法是作用在类上的，那么只需要操作类就可以了，那么如何才能批量的操作定制类呢？这就需要用到类的类，元类。

众所周知，对象 object 是由类 class 实例化得到的，那么类就是对象的定义类型。

由此可知，类有没有定义类型呢，类的基类，万物的初始是什么呢？那就是类型 type 。

在 Python 中，使用 `type` 方法能够看到对象的类，比如 `type(1)` 是 `int`, `type('1')` 是 `str` ，那么 `type(str)` 就能得到类的类 `type`
> 这里只针对 新式类，不考虑 老式类

```
>>> type(1)
<class 'int'>
>>> type('1')
<class 'str'>
>>> type(str)
<class 'type'>
>>> class Foo(object):
...     pass
...
>>>
>>> type(Foo())
<class '__main__.Foo'>
>>> type(Foo)
<class 'type'>
```

其实类的类，就是 `type` ，也叫元类，一般场景下，不会针对元类进行处理，如果你不知道为什么要使用元类，那就不要使用元类。

```
                +----------------+
                |    元类(type)  |
                +---------------+
                      |
                      |实例化
                      v
                +---------------+
                |    类(class)  |
                +---------------+
                      |
                      |实例化
                      v
                +----------------+
                |   对象(object)  |
                +----------------+
```

一个元类的简单应用，收集所有子类

```python
# -*- coding: utf-8 -*-

class CollectMeta(type):
    class_collection = []

    def __new__(cls, *args, **kwargs):
        # 类的创建参数，是 (name, bases, attrs), 返回就是一个类
        # return super(CollectMeta, cls).__new__(cls, *args, **kwargs)
        # 可以继承父类创建，也可以使用 type 直接创建
        class_ = type.__new__(cls, *args, **kwargs)
        cls.class_collection.append(class_)
        return class_


class Fruit(object, metaclass=CollectMeta):
    pass


class Apple(Fruit):
    pass


class Orange(Fruit):
    pass


if __name__ == '__main__':
    print(CollectMeta.class_collection)
    print(Fruit.class_collection)
    print(Apple.class_collection)

```

这里会自动收集所有注册上的子类

```
[<class '__main__.Fruit'>, <class '__main__.Apple'>, <class '__main__.Orange'>]
[<class '__main__.Fruit'>, <class '__main__.Apple'>, <class '__main__.Orange'>]
[<class '__main__.Fruit'>, <class '__main__.Apple'>, <class '__main__.Orange'>]
```

那么，到此为止，我们已经基本可以知道一个对象实例化时的大概流程了。

1. `type` 的 `__new__`  生成 `class`
2. `class` 的 `__new__` 生成 `object`
3. `class` 的 `__init__` 初始化 `object`

这里的 `type` 其实在初始化的时候，也会调用 `__init__` 方法，和 `__class__` 的一样，不过这里的初始化对象是针对类对象的。

对于类的基类，metaclass 其实我们需要的主要就是生成类的功能，那么元类就真的需要一个类么？我们是不是可以使用一个方法来实现。

答案毫无疑问是可以的。

```python
# -*- coding: utf-8 -*-


def create_class(name, bases, attrs):
    # 这里的参数就是创建类的三个参数
    new_attrs = attrs.copy()
    for key, value in attrs.items():
        if not key.startswith("__"):
            new_attrs[key.upper()] = value
            del new_attrs[key]
    return type(name, bases, new_attrs)


class Foo(object, metaclass=create_class):
    name = "foo"


class Bar(object, metaclass=create_class):
    name = "bar"


if __name__ == '__main__':
    f = Foo()
    print(f)
    print(f.NAME)
    print(Bar().NAME)

```

这里需注意，`Bar` 不能继承 `Foo`.

因为 `type` 方法的奇怪的原因，只会创建一个类，使用 OOP 中如果不是使用 `type.__new__` 而是使用 `type` 的时候也会出现这个问题。

在这里指定元类的方法是只针对 Python3 的，在 Python2 中使用 `__metaclass__ = create_class` 的方式去注明元类。

可以写在类里，则只针对当前类，如果写在文件里，则针对这个文件内的所有类，针对所有类的话也比较危险，不建议。

一般推荐使用 `six.with_metaclass(type)` 的方式来指定基类，这种方式不支持函数时的元类。

### 调用之后再调用

调用之后再调用有点像链式执行，但是也有一些差异，常见的链式执行还需要再次调用一个方法，比如像这样。

```python
# -*- coding: utf-8 -*-


class Factor(object):
    def __init__(self, origin=0):
        self.origin = origin

    def add(self, x):
        self.origin += x
        return self

    def sub(self, x):
        self.origin -= x
        return self

    def mul(self, x):
        self.origin *= x
        return self

    def div(self, x):
        self.origin /= x
        return self

    def result(self):
        return self.origin


if __name__ == '__main__':
    print(Factor().add(2).add(1).mul(3).sub(1).div(2).result())

```

但是如果只想累加，不想重复调用同一个函数的那种呢？如何进行柯里化(Currying) ？

```python
# -*- coding: utf-8 -*-

from operator import add
from functools import partial


def curry_func(func, origin):
    handle_func = partial(func, origin)

    def inner(*args):
        nonlocal handle_func
        for arg in args:
            result = handle_func(arg)
            handle_func = partial(func, result)
            inner.result = result
        return inner

    inner.result = origin
    return inner


if __name__ == '__main__':
    print(curry_func(add, 1)(1)(2)(3)(5, 6, 7).result)

```

一个函数化的简单例子，那么如何使用 OOP 实现呢？

```python
# -*- coding: utf-8 -*-
from operator import add


class CurrryingFactor(object):
    def __init__(self, func, origin):
        self.func = func
        self.result = origin

    def __call__(self, *args):
        for arg in args:
            self.result = self.func(self.result, arg)
        return self


if __name__ == '__main__':
    print(CurrryingFactor(add, 1)(2)(3)(4, 5, 6).result)

```

好吧，我弄错了，其实这并不是真正的柯里化，真正的柯里化是将多参函数变成多次调用的函数。

```python
# -*- coding: utf-8 -*-


def curry_wrap(func):
    args_list = []

    def inner(*args):
        if not args:
            args = args_list.copy()
            args_list.clear()
            return func(*args)
        args_list.extend(args)
        return inner

    return inner


if __name__ == '__main__':

    curry_add = curry_wrap(triple_add)
    print(curry_add(1, 2, 3)())
    print(curry_add(1)(2, 3)())
    print(curry_add(1)(2)(3)())
    print(curry_add(1, 2)(3)())

```

上面的实现在计算的时候还要清空一下存储的数据，一种更优雅的实现。

```python
# -*- coding: utf-8 -*-
# copied from simplecurry.py

from operator import add
from functools import partial


def quadruple_add(a, b, c, d):
    return a + b + c + d


def curried(fn):
    def wrapped(*args):
        if fn.__code__.co_argcount > len(args):
            return partial(curried(fn), *args)
        else:
            return fn(*args)

    return wrapped


if __name__ == '__main__':
    curried_add = curried(quadruple_add)
    print(curried_add(1, 2, 3, 4))
    print(curried_add(1)(2)(3, 4))
    print(curried_add(1)(2)(3)(4))
    print(curried_add(1, 2)(3)(4))

```

好了，打住，这里的重点不是柯里化，而是 OOP 的实现，对于一个类的实例化对象，还能进行再次的函数调用。

那对于实例对象的调用 `__call__` 函数，这个魔术方法就是和其他的实例方法一样的，只是它没有方法名，它的调用是直接对示例对象进行的。

### 元类实现单例模式

在了解元类实例化成类，类实例化成对象的流程之后，我们就可以继续单例模式的实现了。

```Python
# -*- coding: utf-8 -*-


a_type = type("OneType", (type, ), {})
a_class = a_type("OneClass", (object, ), {})
a_object = a_class()
print(a_type, type(a_type))
print(a_class, type(a_class))
print(a_object, type(a_object))

```

结果是

```
<class '__main__.OneType'> <class 'type'>
<class '__main__.OneClass'> <class '__main__.OneType'>
<__main__.OneClass object at 0x7fc4e91d79d0> <class '__main__.OneClass'>
```

那么，最简化的写法就是 

```python
print(type("OneType", (type,), {})("OneClass", (object,), {})())
```

由此可知，其实类的实例化方法就是元类的调用方法。`object.__new__` == `type.__call__`

只要有这个结论，那么我们的单例元类就出来了。

```python
# -*- coding: utf-8 -*-

class SingletonType(type):
    def __init__(self, *args, **kwargs):
        print("init class")
        super(SingletonType, self).__init__(*args, **kwargs)
        self._instance = None

    def __call__(self, *args, **kwargs):
        print("call type, new object")
        if not self._instance:
            self._instance = object.__new__(self, *args, **kwargs)
            # 或者下面的写法，是等价的
            # self._instance = type.__call__(self, *args, **kwargs)
            # self._instance = super(SingletonType, self).__call__(*args, **kwargs)
        return self._instance

    def __new__(cls, *args, **kwargs):
        print("new class")
        return super(SingletonType, cls).__new__(cls, *args, **kwargs)


class Animal(object, metaclass=SingletonType):
    pass


class Human(object, metaclass=SingletonType):
    pass


class Dog(Animal):
    pass


class Cat(Animal):
    pass


if __name__ == '__main__':
    a = Animal()
    b = Animal()
    c = Cat()
    c2 = Cat()
    d = Dog()
    d2 = Dog()
    h = Human()
    print(a, id(a))
    print(b, id(b))
    print(c, id(c))
    print(c2, id(c2))
    print(d, id(d))
    print(d2, id(d2))
    print(h, id(h))

```

这里针对每个类都是有自己单独的实例对象挂载，每个类的实例化都是单独的一个对象。

```
new class
init class
new class
init class
new class
init class
new class
init class
call type, new object
call type, new object
call type, new object
call type, new object
call type, new object
call type, new object
call type, new object
<__main__.Animal object at 0x7fd1ad734d50> 140538534907216
<__main__.Animal object at 0x7fd1ad734d50> 140538534907216
<__main__.Cat object at 0x7fd1ad73a7d0> 140538534930384
<__main__.Cat object at 0x7fd1ad73a7d0> 140538534930384
<__main__.Dog object at 0x7fd1ad73f390> 140538534949776
<__main__.Dog object at 0x7fd1ad73f390> 140538534949776
<__main__.Human object at 0x7fd1ad7427d0> 140538534963152
```

重点是 `__init__` 和 `__call__` 方法，`__new__` 方法可以不用。

然后这里**不能**偷懒写到一起，这样会导致父子类使用同一个对象

```python
class SingletonType(type):
    def __call__(self, *args, **kwargs):
        if not hasattr(self, "_instance"):
            self._instance = object.__new__(self)
        return self._instance

```

## 参考链接
[Python 动态生成实例](https://windard.com/blog/2019/12/26/Python-Dynamic-Create-Class)
[Python 的内置函数](https://windard.com/project/2016/11/07/Function-In-Python-Class)      
[深入理解Python中的元类(metaclass)](https://www.cnblogs.com/JetpropelledSnake/p/9094103.html)         
[Python 元类 (MetaClass) 小教程](https://lotabout.me/2018/Understanding-Python-MetaClass/)              
[Python 的元类与元编程](https://segmentfault.com/a/1190000023764901)                    
[柯里化](https://zh.wikipedia.org/wiki/%E6%9F%AF%E9%87%8C%E5%8C%96)                    
[柯里化（Currying）](https://zh.javascript.info/currying-partials)            
[高级函数技巧-函数柯里化](https://segmentfault.com/a/1190000018265172)           
[simplecurry](https://pypi.org/project/simplecurry/)                  
[飘逸的python - 单例模式乱弹](https://blog.csdn.net/handsomekang/article/details/46672047)          
[Python 元类详解 __new__、__init__、__call__、__metacalss__](https://www.jianshu.com/p/2e2ee316cfd0)         
[Python元类中的__call__和__new__的区别？](https://segmentfault.com/q/1010000007818814)            
[python中元类的__call__方法的作用](https://blog.csdn.net/tuxinhang/article/details/78742244)         
[Python 元类详解 __new__、__init__、__call__](https://www.cnblogs.com/sidianok/p/14224610.html)        
[Python metaclasses by example](https://eli.thegreenplace.net/2011/08/14/python-metaclasses-by-example)       
[使用元类](https://www.liaoxuefeng.com/wiki/1016959663602400/1017592449371072)           