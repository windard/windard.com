---
layout: post
title: python中的迭代器和生成器
category: project
description: 迭代器 (iterators) 生成器 (generators) 一直傻傻分不清
---

## 可迭代对象

迭代是指重复反馈过程的活动，每一次对过程的重复被称为一次迭代。在 Python 中的对可迭代对象的 `for` 循环遍历被称为迭代，每一次遍历被称为一次迭代。

Python 中的可迭代对象包括列表，元组，字符串，字典，由  `range` 和 `xrange` ，生成的数组对象等。

其中对字典的迭代是对键进行迭代，如果想对其键值对都进行迭代，需要使用字典的 `items` 方法，将其转换为列表中的元组。

在其他编程语言中，多是以下标进行迭代的，但是 Python 中的可迭代对象都没有下边，如果得到迭代值的位置，可以使用 `enumerate` 将其转换为一个带下标的可迭代对象。

判断一个对象是否为可迭代对象可以使用 collections 的 Iterable 判断。  

```
>>> from collections import Iterable
>>> isinstance(enumerate('123'), Iterable)
True
>>> isinstance('123', Iterable)
True
>>> isinstance(123, Iterable)
False
>>> isinstance(range(2), Iterable)
True
>>> isinstance(xrange(2), Iterable)
True
```

在最后，把四个容易混淆的词总结一下，循环，迭代，递归，遍历。

- 循环（loop），指的是在满足条件的情况下，重复执行同一段代码。比如，while 语句。
- 迭代（iterate），指的是按照某种顺序逐个访问列表中的每一项。比如，for 语句。
- 递归（recursion），指的是一个函数不断调用自身的行为。比如，以编程方式输出著名的斐波纳契数列。
- 遍历（traversal），指的是按照一定的规则访问树形结构中的每个节点，而且每个节点都只访问一次。

## 迭代器

可迭代对象中主要包含两种数据类型的对象
1. 集合数据类型，可以直接显示所有的迭代元素，如 `list`, `tuple`, `set`, `dict`, `str`, `range` 等
2. 迭代器类型，不能直接显示所有的的可迭代元素，如 `xrange`, `enumerate`, `iter` 等

任何可迭代对象都可以使用 `for` 循环迭代遍历所有迭代元素。

集合数据类型和迭代器类型之间可以相互转换，迭代器类型被 `list` 或 `tuple` 或 `set` 转换为集合数据类型，直接显示全部迭代元素，集合数据类型也可以被 `iter` 转换为迭代器对象，隐藏迭代元素。 

判断一个对象是否为迭代器类型可以使用 collections 的 Iterator 判断

```
>>> from collections import Iterator
>>> isinstance([1,2,3], Iterator)
False
>>> isinstance((1,2,3), Iterator)
False
>>> isinstance(iter((1,2,3)), Iterator)
True
>>> isinstance(range(3), Iterator)
False
>>> isinstance(xrange(3), Iterator)
False
>>> isinstance(iter(xrange(3)), Iterator)
True
>>> isinstance(enumerate([1,2,3]), Iterator)
True
```

可以看到 `iter` 和 `enumerate` 生成的对象确实是迭代器对象，但是 `xrange` 生成的对象不是也看不见的么，为什么不是迭代器对象呢？

因为迭代器对象的定义并不是仅仅不能看见而已，在 Python 中的迭代器对象是需要实现 `next` (Python2) 或者 `__next__` (Python3) 方法，才算是一个迭代器对象， 可以通过 `Iterator.next()` 或者 `next(Iterator)` 来遍历迭代对象，该方法返回下一个该迭代器对象的下一个迭代元素。

而可迭代对象的定义是需要实现 `__iter__` 方法的对象，才是可以迭代对象，该方法返回一个迭代器对象，或者是实现支持下标索引的 `__getitem__` 方法。

> 字符串对象并没有实现 `__iter__` 方法，然而实现了 `__getitem__` 方法，所以也是可迭代对象 

所以实现 `__iter__` 或 `__getitem__` 方法的对象才是可迭代对象，实现了 `__next__` 或 `next` 方法的可迭代对象才是迭代器对象。

> 迭代器对象一定是可迭代对象，可迭代对象不一定是迭代器对象

```
>>> dir([1,2,3])
['__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__delslice__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getslice__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__setslice__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']
>>> dir((1,2,3))
['__add__', '__class__', '__contains__', '__delattr__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__getslice__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'count', 'index']
>>> dir('123')
['__add__', '__class__', '__contains__', '__delattr__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__getslice__', '__gt__', '__hash__', '__init__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '_formatter_field_name_split', '_formatter_parser', 'capitalize', 'center', 'count', 'decode', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'index', 'isalnum', 'isalpha', 'isdigit', 'islower', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']
>>> dir(iter((1,2,3)))
['__class__', '__delattr__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__iter__', '__length_hint__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'next']
>>> dir(iter([1,2,3]))
['__class__', '__delattr__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__iter__', '__length_hint__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'next']
>>> dir(range(3))
['__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__delslice__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getslice__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__setslice__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']
>>> dir(xrange(3))
['__class__', '__delattr__', '__doc__', '__format__', '__getattribute__', '__getitem__', '__hash__', '__init__', '__iter__', '__len__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
>>> dir([i for i in xrange(3)])
['__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__delslice__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getslice__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__setslice__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']
>>> dir((i for i in xrange(3)))
['__class__', '__delattr__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__iter__', '__name__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'close', 'gi_code', 'gi_frame', 'gi_running', 'next', 'send', 'throw']
```

可以看到这些都定义了 `__iter__` 或 `__getitem__` 方法，即为可迭代对象，但是并非所有都有 `next` 方法，其中只有三个是迭代器对象。

> 同样的列表生成器，使用 `[]` 的是集合数据类型对象，使用 `()` 就是迭代器对象。 <br>
> 这样的的生成式被称为生成器解析式，在内置函数中使用时可以不加 `()` 如 `sum(i*i for i in range(10))`

### 迭代器的使用

同样的可迭代对象，但是迭代器相对于集合数据类型一个显著的好处就是不用一次性将全部迭代元素加载到内存中，而是可以实现随用随取，它是以一种延迟计算的方式返回元素。

对于一个迭代器对象可以使用 `next(Iterator)` 或者是 `Iterator.next()` 来取得下一个迭代元素，直到取出全部元素，返回 `StopIteration` 错误。

```
>>> a = enumerate([1,2,3])
>>> a.next()
(0, 1)
>>> next(a)
(1, 2)
>>> a.next()
(2, 3)
>>> next(a)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

但是当我们使用 `for` 循环来取出迭代器对象的全部迭代元素时，却不会抛出 `StopIteration` 错误，因为 for 循环已经替我们做了异常处理。

那么现在我们自己来实现一个迭代器对象，也就是只需要实现 `__iter__` 和 `next` 方法即可。

```
# coding=utf-8


class MyRange(object):

    def __init__(self, n):
        self.i = 0
        self.n = n

    def __iter__(self):
        return self

    def next(self):
        if self.i < self.n:
            i = self.i
            self.i += 1
            return i
        else:
            raise StopIteration()

if __name__ == '__main__':

    from collections import Iterable, Iterator

    print isinstance(MyRange(3), Iterable)
    print isinstance(MyRange(3), Iterator)
    print MyRange(3)
    print list(MyRange(3))
    for i in MyRange(3):
        print i,

```

输出

```
True
True
<__main__.MyRange object at 0x029D1070>
[0, 1, 2]
0 1 2
```

那我们再来实现一个经典的斐波那契迭代器对象

```
# coding=utf-8


class Fib(object):

    def __init__(self, n):
        self.a = 0
        self.b = 1
        self.n = n

    def __iter__(self):
        return self

    def next(self):
        fib = self.a
        if fib > self.n:
            raise StopIteration()
        self.a, self.b = self.b, self.a + self.b
        return fib

if __name__ == '__main__':

    fib = Fib(5)
    print fib.next(),
    print next(fib),
    for i in fib:
        print i,

```

输出

```
0 1 1 2 3 5
```

或者这样的斐波那契数列

```
# coding=utf-8


class Fib(object):

    def __init__(self, n):
        self.a = 0
        self.b = 1
        self.n = n

    def __iter__(self):
        return self

    def next(self):
        if self.n:
            fib = self.a
            self.a, self.b = self.b, self.a + self.b
            self.n -= 1
            return fib
        raise StopIteration()

if __name__ == '__main__':

    fib = Fib(5)
    print fib.next(),
    print next(fib),
    for i in fib:
        print i,

```

在 Python 2 中的很多返回数据集合类型的的内置函数，在 Python 3 中都改为了返回迭代器，在海量数据计算中，使用迭代器更方便。

在 Python 标准库 itertools 中有很多的迭代器对象可供使用，在某些地方可能更加方便。

## 生成器

生成器本质上也是一种迭代器，在上文中的迭代器实现是否觉得太麻烦了呢？需要定义一个类，然后实现两个方法，才能得到一个迭代器，而如果使用生成器的话，将非常容易。

生成器使用 `yield` 关键字，在函数返回值的时候不再使用 `return` 关键字，这样的函数被称为生成器函数。函数被调用时返回一个生成器对象，然后使用 `next(Generator)` 或者 `Generator.next()` 来获得函数返回值。

生成器对象在被生成的时候，函数实际上并没有被执行，只有在使用 `next(Generator)` 或者 `Generator.next()` 时才被执行，返回执行结果，然后在下一次被调用时，从上一个 `yield` 返回的地方继续执行，得到下一个返回值，直到结束抛出 `StopIteration` 错误。

``` 
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

### 生成器的使用

显然使用生成器比迭代器简洁方便，更加优雅，使用生成器实现斐波那契数列。

```
# coding=utf-8


def fib(n):
    a, b = 0, 1
    while n > a:
        yield a
        a, b = b, a + b

if __name__ == '__main__':

    from collections import Iterable, Iterator

    f = fib(5)

    print isinstance(f, Iterable)
    print isinstance(f, Iterator)

    print f.next(),
    print f.next(),
    print next(f),
    for i in f:
        print i,
```

输出

```
True
True
0 1 1 2 3
```

或者这样的斐波那契数列

```
# coding=utf-8


def fib(n):
    a, b = 0, 1
    while n:
        yield a
        a, b = b, a + b
        n -= 1

if __name__ == '__main__':

    from collections import Iterable, Iterator

    f = fib(5)

    print isinstance(f, Iterable)
    print isinstance(f, Iterator)

    print f.next(),
    print f.next(),
    print next(f),
    for i in f:
        print i,
```

或者输出杨辉三角

```
# coding=utf-8


def triangles(n):
    result = [1]
    while n:
        yield result
        data = result[:]
        for i in xrange(1, len(data)):
            result[i] = data[i-1] + data[i]
        result.append(1)
        n -= 1

if __name__ == '__main__':

    for i in triangles(10):
        print i

```

## 高级生成器

在 Python 2.5 之后，`yield` 不但是一个关键字，还是一个表达式。

在使用 `yield` 的时候，首先是返回一个生成器，通过 `next` 来生成下一个结果。现在，`yield` 关键字不仅可以用来输出执行结果，还可以从外界获得输入 。

生成器的 `send` 方法来向生成器内部输入的方法，同时唤醒生成器继续执行，输出执行结果。

如果使用高级生成器，则第一次必须使用 `next` 或者 `send(None)` 获得第一次输出，然后用 `send` 方法输入参数，正常执行获得输出。

所以 `for` 将不能循环遍历生成器，也无法从迭代器转换为集合类型数据对象，但是生成器解析式还可以使用，只不过得到了一个新的高级生成器。

生成器的 `close` 方法用来结束生成器，结束之后调用 `next` 或者 `send` 都会抛出 `StopIteration` 错误。

在生成器的最后，如果不主动 `close` ，它可以使用 `send` 函数无穷无尽。

这是普通的生成器 

```
# coding=utf-8


def MyRange(n):
    i = 0
    while i < n:
        yield i
        i += 1

if __name__ == '__main__':

    from collections import Iterable, Iterator

    print isinstance(MyRange(3), Iterable)
    print isinstance(MyRange(3), Iterator)
    print MyRange(3)
    print list(MyRange(3))
    for i in MyRange(3):
        print i,
```

输出 

```
True
True
<generator object MyRange at 0x029B5DA0>
[0, 1, 2]
0 1 2
```

这是高级生成器

```
# coding=utf-8


def MyRange(n):
    i = 0
    while i < n:
        i = (yield i)
        i += 1

if __name__ == '__main__':

    from collections import Iterable, Iterator

    print isinstance(MyRange(3), Iterable)
    print isinstance(MyRange(3), Iterator)
    print MyRange(3)
    print dir(MyRange(3))
    my_range = MyRange(5)
    # 第一次使用 send(None) 也可
    # print my_range.send(None)
    print my_range.next()
    print my_range.send(1)

    # 报错 TypeError
    # print my_range.next()
    print my_range.send(2)

    # 报错 TypeError
    # print my_range.next()

    # 报错 StopIteration
    # print my_range.send(5)

    my_range.close()

    # 报错 StopIteration
    # print my_range.next()
    # print my_range.send()

    # 报错 TypeError
    # print list(MyRange(3))

    # 报错 TypeError
    # for i in MyRange(3):
    #     print i,

    print
    myRange = MyRange(3)
    print myRange == iter(myRange)

    # 报错 TypeError
    # print [i for i in myRange]

    print (i for i in myRange)

```

输出

```
True
True
<generator object MyRange at 0x028C5EB8>
['__class__', '__delattr__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__iter__', '__name__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'close', 'gi_code', 'gi_frame', 'gi_running', 'next', 'send', 'throw']
0
2
3

True
<generator object <genexpr> at 0x028D75A8>
```

或者这样的高级生成器

```
# coding=utf-8


def echo(n):
    while True:
        n = (yield n)

if __name__ == '__main__':

    c = echo('hello')

    print c.send(None)
    print c.send('world!')
    print c.next()
    print c.send('...')
    # 报错 TypeError
    # print c.send()
```

输出

```
hello
world!
None
...
```

在生成器函数中 `n = (yield n)` 并不一定需要 `()` ，只是一般习惯。`send` 函数必须输入数据，哪怕只是 `None` 。

在高级生成器中 `next` 函数并不是必须的，主要都是由 `send` 函数驱动，在本人看来，高级生成器与原来的生成器已经不再是同一种生成器。

高级生成器与普通生成器各有利弊，不做评判，不过高级生成器由 `send` 驱动的优势在 协程 中展现出了巨大作用。

### 高级生成器应用

之前我用线程写过生产者消费者模型，需要用到资源锁，就比较复杂，用协程就比较容易实现，这是使用高级生成器实现的协程。

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

输出

```
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
