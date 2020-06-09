---
layout: post
title: Python 的内置函数
category: project
description: 完成上一篇 Python 的内置函数的关于 Python 的类未完成部分。
---

## Python 的面向对象特性

在 [Python 继承中的构造方法和成员方法](https://windard.com/blog/2016/03/01/Method-In-Python-Child) 一文中已经对 Python 的类的一些特性有一个简单的介绍。

### Python 的类属性和实例属性

对于面向对象编程语言来说，类就像模具，使用这个模具新建一个对象即为实例，在 Python 中亦然。

在 Java 语言中，只能给实例绑定属性，在 Java 中也被称为变量，分为私有变量，公有变量，静态变量等几类。

但是在 Python 中既可以给实例绑定属性，也可以给类绑定属性。

在给实例绑定的实例属性在 `__init__` 构造函数中声明，或者在函数实例中定义，而类属性则在类的定义之内，类的函数之外声明。

类可以直接访问类属性，但是不能访问实例属性。实例可以访问实例属性，也能访问类属性。

```
# coding=utf-8

class Student(object):
    grade = 5
    def __init__(self, name):
        self.name = name

# Student 的类属性
print "Student.grade",Student.grade

# Student 无法使用实例属性，会报错 AttributeError
# print "Student.name",Student.name

Mary = Student('Mary')

# 实例可以访问类属性，也能访问实例属性
print "Mary.grade",Mary.grade
print "Mary.name",Mary.name

# 类修改类属性
# 在实例未修改类属性之前，实例的类属性与类的类属性指向同一位置
Student.grade += 1

print '-'*20
print 'After School.grade += 1'
print "Student.grade",Student.grade
print "Mary.grade",Mary.grade

# 实例修改类属性
# 实例修改类属性后变为实例属性
# 实例的实例属性与类的类属性分离，指向不同位置
Mary.grade += 1

print '-'*20
print 'After Mary.grade += 1'
print "Student.grade",Student.grade
print "Mary.grade",Mary.grade

# 新增一个实例
# 新增实例的类属性在未修改之前仍与与类的类属性仍指向同一位置
John = Student('John')

print '-'*20
print 'After John join'
print "John.grade",John.grade

# 新增实例修改类属性
# 新增实例修改类属性后变为实例属性
# 此时原实例，新增实例的类属性和类三者的类属性分别指向三个不同位置
John.grade += 2

print '-'*20
print 'After John.grade += 2'
print "John.grade",John.grade
print "Mary.grade",Mary.grade
print "Student.grade",Student.grade

# 实例将类属性赋值
Mary.grade = 10

# 此时原实例，新增实例的类属性和类三者的类属性分别指向三个不同位置
print '-'*20
print 'After Mary.grade = 10'
print "John.grade",John.grade
print "Mary.grade",Mary.grade
print "Student.grade",Student.grade

# 删除实例的实例属性
del Mary.grade

# 此时实例的实例属性即从实例属性退回类属性
# 则实例的类属性与类的类属性指向同一位置
# 新增实例实例属性和类的类属性仍然指向不同位置
print "-"*20
print 'del Mary.grade'
print "John.grade",John.grade
print "Mary.grade",Mary.grade
print "Student.grade",Student.grade

# 无法删除实例的类属性
# del Mary.grade

# 可以删除类的类方法
del Student.grade

# 此时类与实例都无法使用类属性
# 仅有新增实例可以使用实例属性
print "-"*20
print 'del Student.grade'
print "John.grade",John.grade
# print "Mary.grade",Mary.grade
# print "Student.grade",Student.grade

# 若还有新实例生成
# 新实例和原实例和类依旧没有类属性
# 仅有新增属性可以使用实例属性
Tomy = Student('Tomy')

print '-'*20
print 'After Tomy join'
# print "Tomy.grade",Tomy.grade
print "John.grade",John.grade
# print "Mary.grade",Mary.grade
# print "Student.grade",Student.grade

# 若此时仅为新实例赋值，仅为新实例的实例方法
# 并不能为原实例和类恢复类方法
Tomy.grade = 15

print '-'*20
print 'After Tomy.grade = 15'
print "Tomy.grade",Tomy.grade
print "John.grade",John.grade
# print "Mary.grade",Mary.grade
# print "Student.grade",Student.grade

# 在类为其类属性赋值之后
# 原有的类属性才能恢复
Student.grade = 12

print '-'*20
print 'After Student.grade = 12'
print "Tomy.grade",Tomy.grade
print "John.grade",John.grade
print "Mary.grade",Mary.grade
print "Student.grade",Student.grade
```

在上面的例子中School 即为类，Mary, John 和 Tomy 即为实例，grade 即为类属性，name 即为实例属性。

在实例修改类属性前，所以的实例与类共享一个类属性，如果实例修改类属性，则类属性变为实例属性，为其分配新的内存空间。

实例可以删除实例属性，无法删除类属性，只有类才能删除类属性，此时如果新一个生成的实例无类属性。

在实例方法中使用类属性，则使用 `类名.类属性` 来引用，若无重名实例属性的话，也能用 `self.类属性`来引用，在类方法中使用类属性，则使用 `cls.类属性` 来引用。使用实例属性，则使用 `self.实例属性`，`self` 指自身实例。

类属性在每生成一个新实例时并不改变，故可以作为静态属性，作计数器使用。

```
# coding=utf-8

class Student(object):
    num = 0
    def __init__(self, name):
        Student.num += 1
        self.name = name

for x in xrange(10):
    a = Student('fake')

print Student.num
```

在实例属性的操作时，除了可以用 `self` 来指引实例属性之外，还可以使用 `hasattr` 来判断是否有这个实例属性，使用 `setattr` 来生成实例属性，使用 `getattr` 来获得实例属性，使用 `delattr` 来删除实例属性。

```
# coding=utf-8

class Student(object):

    def __init__(self, name):
        self.name = name

Mary = Student("Mary")

if not hasattr(Mary, "age"):
    setattr(Mary, "age", 21)

if hasattr(Mary, "age"):
    print getattr(Mary, "age")

if hasattr(Mary, "age"):
    delattr(Mary, "age")

if not hasattr(Mary, "age"):
    print "End"
```

#### 一些特殊类属性

旧式类没有这么多的类属性，默认都是新式类

- `__dict__`  : 类的类属性（包含一个字典，由类的数据属性组成）
- `__doc__` : 类的说明文档，即定义类时的注释
- `__name__` : 类的名字
- `__file__` : 类所在的完整文件地址
- `__base__` : 类的父类
- `__bases__` : 类的父类们
- `__subclasses__`: 类的子类们
- `__module__` : 类所在的模块，在主文件中即为 `__main__`
- `__class__` : 类的类型
- `__str__` : 打印显示效果
- `__repr__` : 默认显示效果

#### 一些特殊的实例属性

- `__class__` : 实例的类
- `__dict__` : 实例的实例属性
- `__doc__` : 实例的说明文档，同 类的说明文档

### 私有属性和私有方法

私有属性与其他面向对象编程语言中的私有变量意思一致，只是表现形式不一致，在 Python 中使用双下划线 `__` 加变量名表示私有属性。

私有属性分为 私有类属性 和 私有实例属性。

```
# coding=utf-8
class School(object):
    __location = 'Shannxi'

    def __init__(self, name):
        self.__name = name

    def where(self):
        print School.__location

    def what(self):
        print self.__name

xidian = School('Xidian')
xidian.where()

# 在外部无法通过类来访问私有类属性
# 在外部无法通过实例来访问私有类属性
# print School.__location
# print xidian.__location

# 在外部无法通过实例来访问私有实例属性
# print xidian.__name

# 只有通过变换形式之后才能访问私有类属性
print School._School__location
print xidian._School__location

# 只有通过变换形式后才能访问私有实例属性
print xidian._School__name
```

私有方法同样的也是双下划线 `__` 加变量名，只能在类的内部访问。

子类也无法调用父类的私有方法和私有属性。

但是同样的，私有方法并不绝对私有，在外界可以通过单下划线加类名加私有方法的方式访问，虽然这是不应该的。

### 类的静态方法和类方法

静态方法和类方法都是采用装饰器来实现，但是静态方法的关键词是 `staticmethod` ，类方法的关键词是 `classmethod` 。

Python 中常见的三种方法即为实例方法，静态方法和类方法。

实例方法即为在类中定义的，第一个参数为 `self` 的，可以调用类属性和实例属性，只能由实例调用的方法。

静态方法即为使用 `@staticmethod` 装饰的，参数不限，可以由类或者实例调用，无法通过 `cls` 调用类的属性，不过可以通过 `类名.类属性` 来调用类属性，与一个普通的函数无异的方法。

类方法即为使用 `@classmethod` 装饰的，第一个参数为 `cls` ，表示对自身类的引用，可以使用类的类属性，可以由类或实例调用的方法。

```
# coding=utf-8
class Student(object):
    school = 'xidian'
    def __init__(self, name):
        self.name = name

    @staticmethod
    def write(name):
        print "Hello,", name

    @classmethod
    def judge(cls, words):
        print cls.school,'is', words


# 类或者实例都可以调用静态方法
Student.write('world')
Student('Mary').write('windard')

# 类或者实例都可以调用类方法
Student.judge('bad')
Student('Mary').judge('good')
```

### 类的属性

类的属性和类的方法并不是完全独立的，可以将类的方法想类的属性一样调用，也可以将类的属性像类的方法一样获取。

这里底层实现是使用魔术方法 `__set__` 和 `__get__` ，但是 Python 已经给我们封装好了，直接使用 `property` 和 `setter` 即可方便使用。

property 只能在新式类上使用。

```
# coding=utf-8

import hashlib


class User(object):
    password = ''
    password_hash = ''

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = hashlib.sha512(password).hexdigest()

student = User()
student.password = '123456'

try:
    print student.password
except AttributeError, e:
    print tuple(e)

print student.password_hash

```

### 将实例变成函数

在 Python 中一切皆对象，函数也是对象，函数可以被调用，所以被称为可调用对象。

```
>>> a=abs
>>> type(a)
<type 'builtin_function_or_method'>
>>> isinstance(a, object)
True
>>> a(-1)
1
>>> a.__name__
'abs'
```

我们定义一个类之后，这个类本身也是一个对象，将这个类实例化之后生成的实例还是一个对象，只不过这个类可以被调用，而一般的实例则不能被调用。

```
>>> class foo():
...     pass
...
>>> isinstance(foo, object)
True
>>> bar=foo()
>>> isinstance(bar, object)
True
>>> bar()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: foo instance has no __call__ method
```

可以看到，它报错的原因就是没有 `__call__` 函数，这个函数就是连接实例和函数之间的桥梁，给类实现一个 `__call__` 方法，则可以调用这个实例。

```
>>> class foo():
...     def __call__(self):
...             print "hello world"
...
>>> bar=foo()
>>> bar()
hello world
>>> bar()
hello world
```

就像这样，我们来试一下斐波那契数列

```
>>> class Fib(object):
...     def __call__(self, num):
...             a,b = 0,1
...             self.l = []
...             for i in xrange(num):
...                     self.l.append(a)
...                     a,b = b,a+b
...             return self.l
...
>>> f = Fib()
>>> f(10)
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

这样就进一步模糊了对象和函数之间的界限，至于这个类是继承 object 或者不继承，则是 Python 中新式类和旧式类的区别了，建议用新式类，具体区别下次再讲。

## 上下文管理器

在 Python 中有一个很重要的部分即是上下文管理器，比如说我们想要计算某个函数的运行时间。

```
# coding=utf-8
import time

class ElapsedTime(object):
    def __enter__(self):
        self.start_time = time.time()

    def __exit__(self, exception_type, exception_value, traceback):
        self.end_time = time.time()
        print "Speeds %f S."%(self.end_time - self.start_time)

def countsum(count):
    num = 0
    for x in xrange(count):
        num += x
    return num

with ElapsedTime():
    print countsum(100000)
```

这个也可以用装饰器来实现

```
# coding=utf-8
import time


def ElapsedTimeWarp(func):
    def spendtime(*args, **kwargs):
        start_time = time.clock()
        result = func(*args, **kwargs)
        end_time = time.clock()
        print "Speeds %f S." % (end_time - start_time)
        return result
    return spendtime


@ElapsedTimeWarp
def countsum(count):
    num = 0
    for x in xrange(count):
        num += x
    return num

print countsum(100000)

```

感觉上下文管理器跟闭包函数比较类似，所以其实也可以这样写

```
# coding=utf-8
import time


def ElapsedTimeWarp(func):
    def spendtime(*args, **kwargs):
        start_time = time.clock()
        result = func(*args, **kwargs)
        end_time = time.clock()
        print "Speeds %f S." % (end_time - start_time)
        return result
    return spendtime


def countsum(count):
    num = 0
    for x in xrange(count):
        num += x
    return num

print ElapsedTimeWarp(countsum)(100000)

```

除了计算时间，这种补充代码与主代码无关联的情况，即使是在有共享变量的情况下，如文件的打开和关闭的情况，闭包，装饰器和上下文管理器都是可以互换的。

```
# coding=utf-8

class OpenContext(object):
    """docstring for OpenContext"""
    def __init__(self, filename, mode):
        self.fp = open(filename, mode)

    def __enter__(self):
        return self.fp

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fp.close()

with OpenContext('test.txt', "r") as f:
    print f.read()

print '-' * 80


def OpenDecorator(func):
    def OpenFile(filename, mode):
        filename = open(filename, mode)
        func(filename, mode)
        filename.close()
    return OpenFile


@OpenDecorator
def test_Decorator(filename, mode):
    print filename.read()

test_Decorator('test.txt', 'r')

print '-' * 80


def OpenClosure(func):
    def OpenFile(filename, mode):
        filename = open(filename, mode)
        func(filename, mode)
        filename.close()
    return OpenFile


def test_Closure(filename, mode):
    print filename.read()

OpenClosure(test_Closure)('test.txt', 'r')

```

上下文管理器一般用在 文件打开自动关闭，线程锁获取自动释放，数据库钩子获取自动释放等地方。

如线程锁获取自动释放的实现，和文打开自动关闭的上下文管理器

```
# coding=utf-8

import threading

class LockContext(object):
    """docstring for LockContext"""
    def __init__(self):
        print "__init__"
        self.lock = threading.Lock()

    def __enter__(self):
        print "__enter__"
        self.lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print "__exit__"
        self.lock.release()

with LockContext():
    print "in the context"

class OpenContext(object):
    """docstring for OpenContext"""
    def __init__(self, filename, mode):
        self.fp = open(filename, mode)

    def __enter__(self):
        return self.fp

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fp.close()

with OpenContext("/tmp/a", "a") as f:
    f.write("hello world ~ ")

```

## 优雅显示

Python 的默认显示只能输出在内存中的位置，但是这对我们来说一般都没有什么用，可以让它更优雅的显示。

```
>>> class Foo(object):
...     def __init__(self, id, name):
...             self.id = id
...             self.name = name
...
>>> bar = Foo(1,'bar')
>>> bar
<__main__.Foo object at 0x02ED09B0>
>>> print bar
<__main__.Foo object at 0x02ED09B0>
```

我们可以让其优雅的显示出来

```
>>> class Foo(object):
...     def __init__(self, id, name):
...             self.id = id
...             self.name = name
...     def __str__(self):
...             return '({}, {})'.format(self.id, self.name)
...     def __repr__(self):
...             return '{}({}, {})'.format(self.__class__.__name__, self.id, self.name)
...
>>> bar = Foo(1,'bar')
>>> bar
Foo(1, bar)
>>> print bar
(1, bar)
>>> str(bar)
'(1, bar)'
>>> repr(bar)
'Foo(1, bar)'
```

这样显得优雅一些。

优雅显示的办法有很多，还可以直接让其显示效果相同即可。

```
>>> class Foo(object):
...     def __init__(self, id, name):
...             self.id = id
...             self.name = name
...     def __str__(self):
...             return '({}, {})'.format(self.id, self.name)
...     __repr__ = __str__
...
>>> bar = Foo(1, '中文')
>>> bar
(1, 中文)
>>> print bar
(1, 中文)
>>> print str(bar)
(1, 中文)
>>> print repr(bar)
(1, 中文)
```

## 闭包

先来看一个闭包的典型应用

```
>>> def mul(factor):
...     def mulfactor(number):
...             return number*factor
...     return mulfactor
...
>>> double=mul(2)
>>> double(4)
8
>>> double(5)
10
```

通过一个嵌套，将另一个函数嵌入到原函数中，调用原函数时，返回另一个函数，但是因为另一个函数处于原函数中，所以仍然保留原函数的局部变量，通过函数嵌套即实现了闭包。

闭包的功能就是通过两个函数的嵌套实现局部变量的持久化存储，将局部变量的作用域扩大到每一次原函数的调用中，在本例中类似于默认参数的使用，或者是默认参数加上装饰器的使用，但是实际中的闭包用途更加广泛 。

## 新式类和旧式类

想要理解新式类和旧式类的关系，可以先了解一下 对象 (object)和类型 (type), 类 (class) 和类型 (type) 的区别。

在面向对象程序语言中有两种关系：
1. 继承关系，子类继承父类的一些属性和方法
2. 实现关系，实例化一个类，以某个类为模板实例化一个对象，对象是类的一个实例

查看继承关系可以使用 `__class__` 查看自己的类，或者 `__base__` 查看自己的父类

查看实现关系，可以 `isinstance` 查看自己是谁的实例

Python 是属于一门面向对象的程序语言，所以 Python 中也是 一切皆对象 的，所有的类或者实例或者函数或者其他数据类型的父类都是 object 。

那么 type 是什么呢？type 是实现关系的顶端，所有的对象都是它实例化的，所以当然也包括 object。

感觉有点像是先有鸡还是先有蛋的问题，是先有 object 还是先有 type 呢？

我们先来看一下是不是一切皆对象，即一切数据类型都是 object 的实例，或者说一切数据类型的直接父类或者最终父类都是 object。

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
print isinstance(object, object)              # True
```

一切数据类型都是 object 的实例，甚至 object 都是 object 的实例。

```
# print 1.__class__                         # SyntaxError
print type(1)                               # <type 'int'>
print 'a'.__class__                         # <type 'str'>
print [].__class__                          # <type 'list'>
print ().__class__                          # <type 'tuple'>
print {}.__class__                          # <type 'dict'>
print int.__class__                         # <type 'type'>
print str.__class__                         # <type 'type'>
print set.__class__                         # <type 'type'>
print list.__class__                        # <type 'type'>
print dict.__class__                        # <type 'type'>
print type.__class__                        # <type 'type'>
print object.__class__                      # <type 'type'>

# print 1.__base__                          # SyntaxError
# print 'a'.__base__                        # AttributeError
# print [].__base__                         # AttributeError
# print ().__base__                         # AttributeError
# print {}.__base__                         # AttributeError
print int.__base__                          # <type 'object'>
print str.__base__                          # <type 'basestring'>
print str.__base__.__base__                 # <type 'object'>
print list.__base__                         # <type 'object'>
print set.__base__                          # <type 'object'>
print dict.__base__                         # <type 'object'>
print type.__base__                         # <type 'object'>
print object.__base__                       # None
```

虽然当前的类型千差万别，但是他们的所有直接父类或者间接父类都是 object ，而 object 是最终的父类，所以它已经没有父类了，不过还是能有几点发现
1. 未实例化之前都有父类，然而实例化之后就只有类，没有父类
2. 所有的类的类都是 type ， 而实例化对象的类 才是它的类
3. object 的当前类型竟然是 type， object 也是一个类
4. 所有的类型都是形如 `<type XXX>` 的样子

还记得我们前面说的么？ type 是一切实例化对象的顶端，一切对象都是由 type 实例化的。

所以所有的类，无论是直接继承 object，还是间接继承 object 或者就是 object ，它都是 type ，实例化之后生的对象的类才是之前的类。

而类本身，也是一种类型，所以，所有类的类型都是 type 。

那么这样的话，也就是说类才是 type 类型的实例，而已经实例化之后的对象不是 type 类型的实例。

```
print isinstance(1, type)                   # False
print isinstance('a', type)                 # False
print isinstance([], type)                  # False
print isinstance((), type)                  # False
print isinstance({}, type)                  # False
print isinstance(int, type)                 # True
print isinstance(str, type)                 # True
print isinstance(list, type)                # True
print isinstance(set, type)                 # True
print isinstance(dict, type)                # True
print isinstance(type, type)                # True
print isinstance(object, type)              # True
```

在实例化之前的类还是 type 的实例，实例化之后就不再是 type 的实例。

也就是说 在类之上还有一种类，即元类，是类的类。

最终总结：
1. 所有类的最终类型都是 type ，type 是元类
2. 所有类的最终父类都是 object，object 是对象

因为在 Python 的老版本中 对象 (object)和类型 (type) 的界限是模糊不清的，自带的类方法也有很多不同，现在如果没有特殊的原因，建议使用新式类。

在旧式类中，并非所有的类的类型是 type ，但是在新式类中，所有的类的类型都是 type 。

> Python 老版本指 `Python 2.3` 及之前的版本，本文中所有的示例都是在 `Python 2.7` ，所有都是新式类。

使用新式类的方法有两种
1. 继承 `object`，新式类都是直接继承 object ，而旧式类不知道在哪里继承 object
2. 在模块或者脚本开始的地方 `__metaclass__ = type`， 新式类的元类是 type ，而旧式类没有元类

可以查看一下旧式类与新式类的区别

```
# coding=utf-8


class OldClass:
    pass


old_class = OldClass()

# print OldClass.__class__                  # AttributeError
# print OldClass.__base__                   # AttributeError
print old_class.__class__                   # __main__.OldClass
# print old_class.__base__                  # AttributeError

print isinstance(OldClass, type)            # False
print isinstance(OldClass, object)          # True
print isinstance(old_class, type)           # False
print isinstance(old_class, object)         # True


class NewClass(object):
    pass


new_class = NewClass()

print NewClass.__class__                    # <type 'type'>
print NewClass.__base__                     # <type 'object'>
print new_class.__class__                   # <class '__main__.NewClass'>
# print new_class.__base__                  # AttributeError

print isinstance(NewClass, type)            # True
print isinstance(NewClass, object)          # True
print isinstance(new_class, type)           # False
print isinstance(new_class, object)         # True


```

旧式类的类没有类，也没有父类，也不是 type 的实例，旧式类的实例只有类名 ，旧式类和旧式类的实例都是 object 的实例，旧式类也是直接或间接继承自 object。

新式类的类是 type ，父类是 object，所以新式类即使 type 的实例，继承自 object。

同样新式类的实例的类型不再是属于 type 而是新式类，同样没有父类，同样是 object 的实例， 同样也不是 type 的实例。

与以上结果唯一的一点区别是，新式类的实例对象的类是形如 `<class XXX>` ， 而上面的类的实例化对象的类还是形如 `<type XXX>` ，应该作为类型来讲，都是 type 的。

新式类与旧式类的区别还有就是新式类的类属性和类方法明显增加。

```
# coding=utf-8


class OldClass:
    pass


old_class = OldClass()


print OldClass.__dict__
print old_class.__dict__
print type(OldClass)
print type(old_class)

print dir(OldClass)
print dir(old_class)

class NewClass(object):
    pass


new_class = NewClass()


print NewClass.__dict__
print new_class.__dict__
print type(NewClass)
print type(new_class)

print dir(NewClass)
print dir(new_class)
```

输出

```
{'__module__': '__main__', '__doc__': None}
{}
<type 'classobj'>
<type 'instance'>
['__doc__', '__module__']
['__doc__', '__module__']
{'__dict__': <attribute '__dict__' of 'NewClass' objects>, '__module__': '__main__', '__weakref__': <attribute '__weakref__' of 'NewClass' objects>, '__doc__': None}
{}
<type 'type'>
<class '__main__.NewClass'>
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']

```

而在文件开头加上新式类标记 `__metaclass__ = type` 之后，则全文默认都是新式类。

```
# coding=utf-8

__metaclass__ = type


class OldClass:
    pass


old_class = OldClass()

print OldClass.__dict__
print old_class.__dict__
print type(OldClass)
print type(old_class)

print dir(OldClass)
print dir(old_class)


class NewClass(object):
    pass


new_class = NewClass()

print NewClass.__dict__
print new_class.__dict__
print type(NewClass)
print type(new_class)

print dir(NewClass)
print dir(new_class)


```

输出

```
{'__dict__': <attribute '__dict__' of 'OldClass' objects>, '__module__': '__main__', '__weakref__': <attribute '__weakref__' of 'OldClass' objects>, '__doc__': None}
{}
<type 'type'>
<class '__main__.OldClass'>
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
{'__dict__': <attribute '__dict__' of 'NewClass' objects>, '__module__': '__main__', '__weakref__': <attribute '__weakref__' of 'NewClass' objects>, '__doc__': None}
{}
<type 'type'>
<class '__main__.NewClass'>
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
```

## 元类

在上面提到所有的类都是 object 的子类，所有的类都是 type 的实例。

所有实例化对象都是类的实例，都是 object 的间接子类，不再是 type 的间接实例。

在继承中，主要起作用的方法是构造方法 `__init__`， 而在实现的时候，则是实例方法 `__new__` 。

在面向对象程序设计中，设计的最多的就是类，写了各种类，但是，你有没有写过类型呢？

类的类被称为元类，在 Python 中元类只有 type 。新式类与旧式类的区别就在于 有没有类的类。

现在让我们来写一个元类，并让它为称为一个类的类。

```
# coding=utf-8


class MyType(type):
    pass

print MyType.__class__                  # <type 'type'>
print MyType.__base__                   # <type 'type'>


class NewClass(object):
    __metaclass__ = MyType

new_class = NewClass()

print NewClass.__class__                # <class '__main__.MyType'>
print NewClass.__base__                 # <type 'object'>

print new_class.__class__               # <class '__main__.NewClass'>
# print new_class.__base__              # AttributeError

```

现在类的类不再是 type ，而是自定义的 MyType、

在这里也可以发现，它的类型不再是形如 `<type XXX>` 而是形如 `<class XXX>`。

具体的可以看 [Python 的 type 和 object 之间是怎么一种关系？](https://www.zhihu.com/question/38791962) 和 [Python Types and Objects](http://www.cafepy.com/article/python_types_and_objects/python_types_and_objects.html)

## python 的模块

在 Python 模块中常用到的两个函数 `__all__` 和 `__import__`

分别表示在可以引用本模块中的内容，和动态引用另一个模块。

还有 `__file__` 查看模块所在位置，这个也可以在 Python 文件中使用，还可以使用 `__name__` 来查看该文件的所属的 Python 模块名。

## Python 中的魔术方法

### 构造和初始化相关

Python 中有很多神奇的魔术方法，比如说实例函数 `__new__`，`__init__`, `__del__` 等与面向对象有关的魔术方法

在 Python 类的创建过程中，构造函数 `__init__` 并不是作为第一个被调用的函数，首先是调用 `__new__` 实例函数，这才是 Python 对象实例化的第一个函数，其返回值是这个对象的实例，而 `__init__` 没有返回值。

`__new__` 是创建这个类然后返回这个类的实例，而 `__init__` 只是根据传来的参数初始化该实例,两个函数的传入参数除了第一个不同，其他都是相同的,即构造时传入的参数。

一般在设置使用元类的时候才会用到实例函数 `__new__` ，用来控制实例的创建。

比如单例模式的一个常见实现方式，常用于数据库连接池的创建。

```
# coding=utf-8

class Singleton(object):
    def __new__(cls, *args, **kwages):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwages)
        return cls._instance


a = Singleton()
b = Singleton()
print(id(a))
print(id(b))
print a is b
```

`__init__` 和 `__del__` 分别是构造方法和析构方法，和其他的面向对象编程语言一致，不再赘述。

### 对象转换和基本运算相关

- `__cmp__` 定义类比较的魔术方法，在 Python 3 及以后因冗余而被废除
- `__eq__` 定义等于的行为 (equal)
- `__ne__` 定义不等的行为 (not equal)
- `__lt__` 定义小于的行为 (less than)
- `__gt__` 定义大于的行为 (great than)
- `__ge__` 定义大于等于的行为 (great and equal)
- `__le__` 定义小于等于的行为 (less and equal)

在 python 3 之后，没有 `__cmp__` 方法，（也没有 cmp 比较函数），可以用 `functools.total_ordering` 来简化，不需要写着六兄弟了。

以上四个是在类或者函数比较的时候使用

- `__add__` 实现加法的行为
- `__sub__` 实现减法的行为
- `__mul__` 实现乘法的行为
- `__floordiv__` 实现整数除法的行为 `//`
- `__div__` 实现除法的行为 `/` ，在 Python 3 及以后因与 `__truediv__` 相同而被废除
- `__truediv__` 实现真除法，只有在使用 `from __future__ import division` 才会起作用
- `__mod__` 实现取模运算
- `__divmod__` 实现内置的 `divmod()` 运算
- `__pow__` 实现指数运算
- `__lshift__` 实现向左位移操作
- `__rshift__` 实现向右位移操作
- `__and__` 实现按位与操作 `&`
- `__or__` 实现按位或操作 `|`
- `__xor__` 实现按位异或操作 `^`

使用类型转换时的内置函数

- `__int__` 使用 `int()` 转换为整数时的操作
- `__long__` 使用 `long()` 转换为长整型时的操作
- `__float__` 使用 `float` 转换为浮点型的操作
- `__complex__` 使用 `complex()` 转换为复数的操作
- `__oct__` 使用 `oct()` 转换为八进制的操作
- `__hex__` 使用 `hex()` 转换为十六进制的操作
- `__nonzero__` 使用 `bool()` 转换为布尔值的操作在 Python 3 及以后改名为 `__bool__`
- `__coerce__` 使用 `coerce()` 转换为形同数据类型的操作，在 Python 3 及以后因冗余而被废除
- `__index__` 对象使用切片表达式时的操作

其他的内置函数

包括 `str()` `repr()` `unicode()` `hash()` `len()` 等方法都是可以转换为魔术方法 `__str__` `__repr__` `__unicode__` `__hash__` `__len__`,在 Python 3 及以后，`__unicode__` 该废除，新增 `__bytes__`

其中只有可以使用哈希函数获得值得对象才可以作为字典的键值。

### 与对象属性相关

在其他语言中常见的模式方法 `setter()` 和 `getattr` ，在 Python 中是 `__setattr__` 和 `__getattr__` ，设置和获得对象属性，还有一个 `__delattr__` 用来删除对象属性，在使用 Python 关键字 `del ` 时调用。

但是并不是像其他语言中，`setter` 设置的属性使用 `getattr` 获取就好，`__setattr__` 确实是设置属性的，但是 `__getattr__` 并不是真正获得属性的，而是在没有找到属性时才被调用，它用来捕获错误和返回默认值。

真正获取属性的方法是 `__getattribute__` ，用来查找获取属性，定义属性被访问时的行为，所以在访问属性的过程中，先调用 `__getattribute__` 然后调用 `__getattr__`，但是因为属性定义域的原因，并不建议尝试实现 `__getattribute__` 。

设置对象的属性的方法有两种，可以使用 `setattr()` 函数来为对象设置属性，也可以使用 `self.attr=name` 来为对象设置属性，所以在 `__setattr__` 函数内部不能使用以上两种方式来设置属性，会造成递归调用，其实同样的，在使用 `__getattr__` 和 `__getattribute__` 和 `__delattr__` 的时候都需要注意循环调用的问题。

所以，实际上真正的一对是 `__setattr__` 和 `__getattribute__`，并没有 `__setattribute__`，`__getattr__` 只是在错误的时候，未找到的时候才被调用。

```
# coding=utf-8

# 危险，循环调用
# class Computer(object):
#     def __setattr__(self, name, value):
#         self.name = value

#     def __getattr__(self, name):
#         return self.name

# 危险，循环调用
# class Computer(object):
#     def __setattr__(self, name, value):
#         setattr(self, name, value)

#     def __getattr__(self, name):
#         getattr(self, name)

class Computer(object):
    def __setattr__(self, name, value):
        self.__dict__[name] = value
    def __getattr__(self, name):
        return 'not found'
c = Computer()
c.name = 'dell'

print c.name
print getattr(c, 'name')
print dir(c)
print c.__dict__
print c.price
```

结果是

```
dell
dell
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattr__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'name']
{'name': 'dell'}
not found
```

可以看到，给对象增加了属性之后，在对象的属性列表中，不但有实例属性，类属性，还出现了我们为对象新定义的属性，虽然在定义时是将属性定义在 `__dict__` 的字典中，但是在也会出现在对象的属性列表中。

新增加的属性都是在 `__dict__` 字典中。

使用 `__getattribute__` 的效果

```
# coding=utf-8

# 危险，循环调用
# class Computer(object):
#     def __setattr__(self, name, value):
#         self.name = value

#     def __getattr__(self, name):
#         return self.name

# 危险，循环调用
# class Computer(object):
#     def __setattr__(self, name, value):
#         setattr(self, name, value)

#     def __getattr__(self, name):
#         getattr(self, name)

class Computer(object):
    def __setattr__(self, name, value):
        print '__setattr__', name
        self.__dict__[name] = value

    def __getattr__(self, name):
        print '__getattr__', name
        return 'not found'

    def __getattribute__(self, name):
        print '__getattribute__', name
        return super(Computer, self).__getattribute__(name)

c = Computer()
c.name = 'dell'
print '------'
print c.name
print '------'
print getattr(c, 'name')
print '------'
print dir(c)
print '------'
print c.__dict__
print '------'
print c.price
print '------'

```

结果是

```
__setattr__ name
__getattribute__ __dict__
------
__getattribute__ name
dell
------
__getattribute__ name
dell
------
__getattribute__ __dict__
__getattribute__ __members__
__getattr__ __members__
__getattribute__ __methods__
__getattr__ __methods__
__getattribute__ __class__
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattr__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'name']
------
__getattribute__ __dict__
{'name': 'dell'}
------
__getattribute__ price
__getattr__ price
not found
------
```

可以看到 `__getattribute__` 在很多地方被调用了很多次。

```
    def __getattribute__(self, name):
        print '__getattribute__', name
        if name.startswith('__'):
            return getattr(self, name)
        try:
            self.__dict__[name]
        except KeyError:
            self.__getattr__(name)
```

但是这样也是不行的，会循环调用。在取 `self.__dict__` 的时候就是调用自己的 `self.__getattribute__`

### 容器自定义相关

除了可以给对象增加属性之外，也可以直接给对象增加索引。

```
# coding=utf-8

class Mac(object):
    def __setitem__(self, name, value):
        self.name = value
    def __getitem__(self, name):
        return self.name

m = Mac()
m['name'] = 'windard'

print m.name
print m['name']
print dir(m)
print m.__dict__

```

结果是

```
windard
windard
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__getitem__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'name']
{'name': 'windard'}
```

可以看到通过给对象增加属性来存储对象的索引，这样就能将对象的当成字典或者列表一样使用,同样的，对象也还存在删除索引的魔术方法，`__delitem__` ，用来删除对象的某个索引。

当然，容器对象除了可以设置和获取索引之外，还有迭代，反转，是否包含等方法。

- `__iter__` 迭代对象方法
- `__reversed__` 使用 `reversed()` 方法
- `__contains__` 是否包含
- `__missing__` 定义找不到索引的行为

```
# -*- coding: utf-8 -*-
class FunctionalList:
    ''' 实现了内置类型list的功能,并丰富了一些其他方法: head, tail, init, last, drop, take'''

    def __init__(self, values=None):
        if values is None:
            self.values = []
        else:
            self.values = values

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        self.values[key] = value

    def __delitem__(self, key):
        del self.values[key]

    def __iter__(self):
        return iter(self.values)

    def __reversed__(self):
        return FunctionalList(reversed(self.values))

    def append(self, value):
        self.values.append(value)

    def head(self):
        # 获取第一个元素
        return self.values[0]

    def tail(self):
        # 获取第一个元素之后的所有元素
        return self.values[1:]

    def init(self):
        # 获取最后一个元素之前的所有元素
        return self.values[:-1]

    def last(self):
        # 获取最后一个元素
        return self.values[-1]

    def drop(self, n):
        # 获取所有元素，除了前N个
        return self.values[n:]

    def take(self, n):
        # 获取前N个元素
        return self.values[:n]

l = FunctionalList()

l.append(1)
l.append('a')

print l
print l[0]
print l.drop(0)

```

### 会话处理器

使用 `__enter__` 和 `__exit__` 实现会话处理器，也可以使用更方便的上下文管理器库

### 对象调用

在对象实例化之后，再次调用对象方法，使用 `__call__` 魔术方法。

### 对象描述器

使用比较少见，一般采用设置属性或者设置索引的办法。

### 对象属性字段限制

只有对象 `__slots__` 中定义的属性，才能够设置和取值，在类定义中已经设置的也可以。

但是在对实例对象进行其他字段的设置，就会报错。正常对象是可以 `setattr` 设置任何属性的，但是有 slot 限制的就不行，object 对象应该是完全限制了。

参考链接 [介绍Python的魔术方法 - Magic Method](https://segmentfault.com/a/1190000007256392)
