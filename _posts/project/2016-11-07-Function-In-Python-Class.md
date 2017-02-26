---
layout: post
title: Python 的内置函数
category: project
description: 完成上一篇 Python 的内置函数的关于 Python 的类未完成部分。
---

### Python 的面向对象特性

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

在类函数中使用类属性，则使用 `类名.类属性` 来引用，若无重名实例属性的话，也能用 `self.类属性`来引用。使用实例属性，则使用 `self.实例属性`，`self` 指自身实例。

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

#### 一些特殊类属性

- `__dict__`  : 类的类属性（包含一个字典，由类的数据属性组成）
- `__doc__` : 类的说明文档，即定义类时的注释
- `__name__` : 类的名字
- `__file__` : 类所在的完整文件地址
- `__bases__` : 类的父类
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

# 只有通过变化形式后才能访问私有实例属性
print xidian._School__name
```

私有方法同样的也是双下划线 `__` 加变量名，只能在实例内访问。

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
		start_time = time.time()
		result = func(*args, **kwargs)
		end_time = time.time()
		print "Speeds %f S."%(end_time - start_time)
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
```

这样显得优雅一些。