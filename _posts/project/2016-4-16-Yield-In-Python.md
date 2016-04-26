---
layout: post
title: python中的yield关键字
category: project
description: 一直没有弄得很明白，先写下来，明白一点是一点
---

一般python的一些特殊属性在其他的编程语言里都有一些相似的，还有很多是编程语言所通用的，但是yield这个关键字确实唯一只出现在python中，定义一个生成器。

yield首先可以当做一般的return来使用，调用生成yield的函数返回的是一个yield实例，并没有数值，必须先执行next得到函数的第一个返回值，然后再次next，从上一个yield返回的地方继续执行得到第二个返回值，也就是说，在我们调用这个函数的时候函数其实并没有执行，只有在一次次的next中才一步步的执行了函数，最后整个函数执行结束，再执行next函数就会返回StopIteration异常。

``` python
>>> def yield_test():
...     yield 1
...     yield 2
...     yield [1,2]
...
>>> a = yield_test
>>> a
<function yield_test at 0xb6df78b4>
>>> a = yield_test()
>>> a
<generator object yield_test at 0xb6df3dc4>
>>> a.next()
1
>>> a.next()
2
>>> a.next()
[1, 2]
>>> a.next()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration

```

或者是在yield用于生成序列：

```python
>>> def foo():
...     for i in range(4):
...             yield i
...
>>> a = foo()
>>> a
<generator object foo at 0xb70692ac>
>>> a.next()
0
>>> a.next()
1
>>> a.next()
2
>>> a.next()
3
>>> a.next()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration

```