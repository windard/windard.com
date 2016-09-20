---
layout: post
title: python中的yield关键字
category: project
description: 一直没有弄得很明白，先写下来，明白一点是一点
---

## yield 关键字

一般python的一些特殊属性在其他的编程语言里都有一些相似的，还有很多是编程语言所通用的，但是yield这个关键字一般比较多的出现在python中，定义一个生成器。

## 生成器

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

## send 与 next

在使用 yield 的时候，首先是返回一个迭代器，通过 next() 来生成下一个结果。其实，yield 关键字不仅可以生成，还可以从输入中获取。

```
>>> def foo():
...     for i in xrange(10):
...             yield i
...
>>> a = foo()
>>> a
<generator object foo at 0xb70d7324>
>>> a.next()
0
>>> a.next()
1
>>> def bar():
...     n = 0
...     while 1:
...             n = yield n
...
>>> b = bar()
>>> b
<generator object bar at 0xb70d734c>
>>> b.send()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: send() takes exactly one argument (0 given)
>>> b.send(1)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can't send non-None value to a just-started generator
>>> b.next()
0
>>> b.next()
>>> b.send(1)
1
>>> b.send(2)
2
>>> b.next()

```

## 协程

之前我用线程写过生成者消费者模型，需要用到资源锁，就比较复杂，用协程就比较容易实现

```
#coding=utf-8
import time

def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        time.sleep(1)
        r = '200 OK'

def produce(c):
    c.next()
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

if __name__=='__main__':
    c = consumer()
    produce(c)

```

运行结果

```
windard@windard:~/github/Python_Lib/code$ python consumer_coroutinue.py
[PRODUCER] Producing 1...
[CONSUMER] Consuming 1...
[PRODUCER] Consumer return: 200 OK
[PRODUCER] Producing 2...
[CONSUMER] Consuming 2...
[PRODUCER] Consumer return: 200 OK
[PRODUCER] Producing 3...
[CONSUMER] Consuming 3...
[PRODUCER] Consumer return: 200 OK
[PRODUCER] Producing 4...
[CONSUMER] Consuming 4...
[PRODUCER] Consumer return: 200 OK
[PRODUCER] Producing 5...
[CONSUMER] Consuming 5...
[PRODUCER] Consumer return: 200 OK

```
