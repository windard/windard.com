---
layout: post
title: Python 面试总结
category: project
description: 在 Python 方面和工作方面的面试总结
---

## 数据库三大范式

- 第一范式即原子性，字段不可再分割； 数据库中表的每一列都不可分割
- 第二范式即完全依赖，没有部分依赖； 数据库中表的每一列都完全依赖于主键
- 第三范式即没有传递依赖；           数据库中表的每一列没有传递依赖

数据库设计需要符合第一范式和第二范式，为了性能可以违反第三范式。

## 数据库使用推荐
- 数据库中最好不要写nullable=True 的字段，最好是所有的都 nullable=False，然后再设一个默认值 default=0
- 数据库中最好不要删数据，只需要再加一个 is_valid 的字段，这样每次需要删除的时候改这个字段就好
- 数据库中最好加一个 create_at 的字段，你以后会发现很有必要的，字段可以是biginteger，使用时间戳，或者是 timestamp 或者是 datetime

## redis 使用优化

redis 典型的数据类型有 字符串，数组，集合，字典（哈希），有序集合。

redis 的使用场景 数据库，缓存，任务队列的输入和输出等

优化总结

1. 根据业务需要选择合适的数据类型，并为不同的应用场景设置相应的紧凑存储参数。
2. 当业务场景不需要数据持久化时，关闭所有的持久化方式可以获得最佳的性能以及最大的内存使用量。
3. 如果需要使用持久化，根据是否可以容忍重启丢失部分数据在快照方式与语句追加方式之间选择其一，不要使用虚拟内存以及diskstore方式。
> 定时快照仍是存储在内存中，故重启即丢失。语句追加即存储在磁盘文件中，但将每一个命令语句都存储，加载较慢。
4. 不要让你的Redis所在机器物理内存使用超过实际内存总量的3/5。

## MySQL 使用优化

MySQL 存储引擎 InnoDB 和 MyISAM，区别是 MyISAM 没有事务支持，没有外键支持，数据库数据分三个文件存储，在大数据量的情况下使用 InnoDB 更好，但是 MyISAM 有索引缓存，可以全文索引，所以查询检索更快，全文搜索更好。

数据库索引在查找字段上，如果有多个查询条件的情况下，可以使用联合索引，但是使用联合索引的情况下需注意符合最左前缀匹配原则，否则反而可能影响性能。

在数据区分度不大的字段上加索引的意义不大，一万条数据的一二三四五，扫百分之二十和扫全表没区别。

索引在扫描的时候加速，但是在插入的时候建立索引有性能影响，且会让数据库庞大冗余，建立索引需要谨慎。

尽量避免使用外键，保证事务一致性应由业务层去完成，而不是数据库层。因为在数据量大，并发数高的情况下，数据库使用外键操作速度慢，不易水平扩展，容易出现死锁，需要做相关检查。数据库本来就是性能瓶颈，去掉外键更加灵活。

不用外键，则不用联合查询，因为使用联合查询也慢。使用 ORM 的时候，将需要联合查询的字段取出来做程序处理，在设计时可以在 model 层抽象出来作为属性使用。

减少互质操作，减少表锁定等待。 InnoDB 是行锁定， MyISAM 是表锁定。比如使用 MyISAM 的 update ，相互操作之间是相互锁定的。数据库引擎选择上在大量查找操作的时候用 MyISAM ，在大量插入更新操作的时候使用 InnoDB .

## 缓存优化

更新缓存时先更新数据库再刷新缓存。

最好的方法是直接更新缓存，因为快，然后再通过缓存异步更新数据库。

## 应用解耦的好处

1. 抽象，模块化，易于查找，分析问题，便于更换改动，维护成本低，可读性高。
2. 代码复用，模块封装。
3. 低耦合，高内聚。模块之间低耦合，模块内部高内聚。

## web 站点性能优化

1. 提高服务器并发处理能力，多线程，多进程，异步 等
2. 动态内容服务器端缓存
3. 静态内容分布式缓存
4. 浏览器缓存
5. web 服务器缓存和反向代理缓存
6. 前端静态文本内容压缩，域名分离提高并发数
7. 数据库性能优化
8. 负载均衡
9. 动态脚本加速

## 前后端分离

在前后端分离中怎么做登陆状态控制，怎么做跨站请求，怎么做 CSRF 防护。

在登陆状态控制可以用 cookies 或者 token ，登陆状态由后端 session 保存。

用 CROS 做跨站请求，对请求资源做请求来源限制。

CSRF 防护原理和控制

CSRF 在一般的 web 应用中是比不可少的，CSRF 的一个有效防御手段就是使用 token，而作为 API 服务，每个请求中都会带有 token，所以实际上并不用担心 CSRF 的问题。

需要担心的是时间戳的问题，使用 token 时需要设置 token 过期时间，那么 token 设置过期时间之后，在请求参数中是否就可以免除时间戳了呢？应该是不可以的，为了防重放攻击，虽然重放的时候 token 一般已经过期了，但是万一没有呢，时间戳还是需要检验的，但是需要注意一点，服务器上有时间同步服务，用户终端不一定会时间同步，若是接口也为普通用户提供服务，则时间戳的接受范围应在当前时间的两侧都可以，因为误差是均匀分布的。

## flask 启动流程

上下文处理流程，一个程序上下文中有很多的请求上下文，在每一个请求上下文是相互独立的，在 `__storage__` 中保存了不同线程的状态，在 flask 中，有线程，也有协程。

在接收到请求之后，首先根据 WSGI 发送的 environ 变量获取

flask 中的钩子有 `before_request`, `before_first_request`, `after_request`, `teardown_request`, `teardown_appcontext`, `context_processor` after 和 teardown 的区别是 前者只在正常处理请求之后执行，teardown 则无论是否发生异常，都执行。

## Python 内存管理

从三个方面来说,一对象的引用计数机制,二垃圾回收机制,三内存池机制

### 引用计数
python内部使用引用计数，来保持追踪内存中的对象，所有对象都有引用计数，当对象的引用计数归零时，自动被回收，内存被释放。

引用计数增加的情况：
1. 创建一个对象
1. 对象被赋值给其他对象
2. 对象被放入一个容器中（如列表、元组或字典）
3. 对象被作为参数传递给函数

引用计数减少的情况：
1. 超出作用域
2. 使用 del 语句被显式的销毁
3. 对象被重新赋值
4. 对象被移除容器
5. 对象所在容器被销毁

sys.getrefcount() 函数可以获得对象的当前引用计数，当使用某个引用作为参数，传递给 getrefcount() 时，参数实际上创建了一个临时的引用。因此， getrefcount() 所得到的结果，会比期望的多1。

在 Python 中，整数和短小的字符，Python 都会缓存这些对象，以便重复使用，节约内存。

### 垃圾回收 (garbage collection)
1. 当一个对象的引用计数归零时，它将被垃圾收集机制处理掉。
2. 当两个对象a和b相互引用时，del语句可以减少a和b的引用计数，并销毁用于引用底层对象的名称。然而由于每个对象都包含一个对其他对象的应用，因此引用计数不会归零，对象也不会销毁。（从而导致内存泄露）。为解决这一问题，解释器会定期执行一个循环检测器，搜索不可访问对象的循环并删除它们。

### 内存池机制
Python提供了对内存的垃圾收集机制，但是它将不用的内存放到内存池而不是返回给操作系统。
1. Pymalloc 机制。为了加速 Python 的执行效率，Python 引入了一个内存池机制，用于管理对小块内存的申请和释放。
2. Python 中所有小于256个字节的对象都使用 pymalloc 实现的分配器，而大的对象则使用系统的 malloc。
3. 对于Python对象，如整数，浮点数和List，都有其独立的私有内存池，对象间不共享他们的内存池。也就是说如果你分配又释放了大量的整数，用于缓存这些整数的内存就不能再分配给浮点数。

## 进程与线程

进程是资源管理的最小单位，线程是程序执行的最小单元，即线程作为程序调度的基本单位，进程作为资源分配的基本单位。

一个进程可以有很多的线程，多个线程之间共享线程的所有资源，每个线程有自己的堆栈和局部变量。

多进程的优点是真正的并行，各自独立的内存和代码空间。而缺点也是一样的，大量占用内存空间，系统开销大。

多线程的优点是线程之间共享内存，内存占用小，缺点是多进程之间难以管理，会导致线程安全问题，更坑爹的是由于 Python GIL 的存在，并不是真正的并发执行。

多线程之间的通信更方便，同一进程下的线程共享全局变量、静态变量等数据，而进程之间的通信需要以通信的方式（IPC)进行。

多进程程序更健壮，多线程程序只要有一个线程死掉，整个进程也死掉了，而一个进程死掉并不会对另外一个进程造成影响，因为进程有自己独立的地址空间。

## Python 中的 GIL

Python 中的多线程不是真正的多线程，因为有 GIL 的存在，在程序执行的时候实际上同时只有一个线程在运行。

Python 中的全局解释器锁 (Global Interpreter Lock) 是在 CPython 中的阻止多线程并发执行的全局互斥锁。PIL 是在系统级别的互质机制，用来保证在内核上不论有多少个 CPU，在同一时刻只能运行一个线程。虽然 Python 在全局解释器层级上存在全局互斥锁，但是仍然不能保证 Python 的线程安全。

GIL 控制的是字节码，互斥锁控制的是 Python 代码，控制粒度不一样，同一条代码可以被编译为不止一条字节码。

GIL 保证内核在同一个时间片下只有一个 Python 线程在执行，多线程通过轮询快速切换，保证顺序执行。在同一个时间片下是线程安全的，但是不能保证在整个程序的多线程仍然线程安全。

线程的同步与互斥解决的是多线程之间的数据访问正确性问题，而 GIL 是保证在 CPython 解释器下当前时刻只有一个线程在执行。

但是 GIL 并不是不能保证 Python 的线程安全，它保证的是 Python 在内存管理级别线程安全，在粗粒度上的线程安全，在细粒度上的线程安全需要手动使用线程互斥锁来实现。


> In CPython, the global interpreter lock, or GIL, is a mutex that prevents multiple native threads from executing Python bytecodes at once. This lock is necessary mainly because CPython’s memory management is not thread-safe. (However, since the GIL exists, other features have grown to depend on the guarantees that it enforces.)


没有解决方案，只有使用多进程或者协程或者其他 Python 编译器或其他编程语言来避免 GIL。

既然 GIL 是在系统内核级别的进行线程切换，在绝大多数场景下是不会感受到 GIL 的存在的，那么如何使用程序来验证 GIL 的存在呢？

可以通过大量的 CPU 密集型程序来占用线程时间片，屏幕上输出，文件操作都是属于 IO 密集型，因为在 GIL 的线程切换规则是时间片用完 (默认为 100 毫秒)，或者主动进入等待状态，使用 `time.sleep` 或者 IO 密集型操作就会主动进行等待状态。

```
# coding=utf-8

import time
from threading import Thread
from multiprocessing import Process


def ElapsedTimeWarp(func):
    def spendtime(*args, **kwargs):
        start_time = time.clock()
        result = func(*args, **kwargs)
        end_time = time.clock()
        print ("Speeds %f S." % (end_time - start_time))
        return result
    return spendtime


def countdown(n):
    while n:
        n -= 1


def t1(COUNT):
    thread1 = Thread(target=countdown, args=(COUNT,))
    thread1.start()
    thread1.join()


def t2(COUNT):
    thread1 = Thread(target=countdown, args=(COUNT//2,))
    thread2 = Thread(target=countdown, args=(COUNT//2,))
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()


def t3(COUNT):
    p1 = Process(target=countdown, args=(COUNT//2,))
    p2 = Process(target=countdown, args=(COUNT//2,))
    p1.start()
    p2.start()

    p1.join()
    p2.join()

if __name__ == '__main__':
    COUNT = 100000000

    print ('countdown in one thread:', )
    ElapsedTimeWarp(t1)(COUNT)

    print ('countdown use two thread:', )
    ElapsedTimeWarp(t2)(COUNT)

    print ('countdown use two Process:', )
    ElapsedTimeWarp(t3)(COUNT)

```

在我的 4 核 CPU Windows 上 Python 2.7 的结果是

```
λ python threading_gil.py
('countdown in one thread:',)
Speeds 12.345390 S.
('countdown use two thread:',)
Speeds 34.441042 S.
('countdown use two Process:',)
Speeds 9.398608 S.
```

只有多进程实现了真正的并行运算，多线程不但没有并行，反而因为线程切换开销更大。

在 Python 3.2 之后对 GIL 进行了一些改进，现在我们在同样的配置下使用 Python 3.4 试一下

```
λ python34.exe threading_gil.py
countdown in one thread:
Speeds 26.765803 S.
countdown use two thread:
Speeds 23.462489 S.
countdown use two Process:
Speeds 16.947642 S.
```

所以单线程变快了，多线程变慢了，但是基本一致了，我选择多进程。

## python 中的 global

如果在函数中不改变全局变量的值，可以直接使用全局变量，如果需要修改全局变量的值，需要先使用 `global` 引入全局变量。

在局部变量中是会自动引入全局变量的，但是在如果在局部变量中修改全局变量，就需要手动将全局变量引入，因为在局部作用域中修改变量，不知道是全局变量还是本地变量，会触发 UnboundLocalError 异常

```
>>> a = 1
>>> def print_a():
...     print a
...
>>> print_a()
1
>>> def print_a_fail():
...     print a
...     a = 2
...
>>> print_a_fail()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 2, in print_a_fail
UnboundLocalError: local variable 'a' referenced before assignment
>>> def print_a_success():
...     global a
...     print a
...     a = 3
...
>>> a
1
>>> print_a_success()
1
>>> a
3
```


## 协程

协程 (Coroutine)，又称微线程。

## 协程与异步 IO 的关系

比如异步 IO 库 twisted 和 协程库 greenlet

## 新式类与旧式类的区别

1. 新式类继承于 object ， 旧式类则不一定
2. 新式类的元类是 type ， 旧式类没有元类
3. 新式类继承于 object 是 type 的实例。继承使用 `__init__` ，实例使用 `__new__`
4. 新式类的类也有父类和继承关系，旧式类的类没有父类和继承关系，只有在实例化之后才有父类和继承关系
3. 新式类可以使用 super 函数，可以使用 `@property` 设置属性
4. 新式类有更多的属性和方法

## 装饰器和闭包的联系

### 装饰器

装饰器 (decorator) 是设计模式中的一种，也是 Python 中用到的不多的设计模式中的一种。装饰器的常用场景有
1. 事务处理，如性能分析，日志记录，运行时间记录
2. 验证及运行时检查，如 flask 中的错误钩子，信号接收和权限管理

装饰器的作用就是通过抽离函数中与函数功能本身无关的雷同代码复用或者给无法复用的代码添加复用代码来为函数或者对象添加额外的功能。
1. 代码复用
2. 添加功能。

如果装饰器本身需要传入参数，则需要三重嵌套关系，最外一层传参数，第二层传函数，最里为内嵌函数。

### 闭包

闭包 (closure) 是函数式编程的一个重要概念，它同样提高了代码的可重复使用性。当一个内嵌函数引用其外部函数作用域的变量，我们就得到一个闭包函数，闭包是一个将内嵌函数和外部函数连接起来的桥梁。闭包函数一般有以下几个特征
1. 有一个内嵌函数
2. 内嵌函数引用外部函数中的变量
3. 外部函数的返回值是内嵌函数

闭包函数返回的内嵌函数带有外部函数的变量，变量的作用域跟随着闭包函数，这样避免使用全局变量而保存一个中间值长期使用。

但是 Python 的闭包不太规范，在 Python2 中闭包的内嵌函数中可以访问外部函数的变量，但是不能修改，只有在 Python3 中使用 `nonlocal` 关键字在内嵌函数中定义之后，才可以在闭包的内嵌函数中修改外部函数的变量。

一个典型的闭包函数的例子

```
# coding=utf-8

def outter(x):
    temp = 3
    def inner(y):
        nonlocal temp
        temp += 1
        print(temp)
        return x + y + temp
    return inner

func = outter(3)
print(func(4))
print(func(4))

print(outter(4)(3))

```

如果非想要在 Python2 中实现的话，可以使用列表来间接实现

```
# coding=utf-8

def outter(x):
    temp = [3]
    def inner(y):
        temp[0] += 1
        print(temp[0])
        return x + y + temp[0]
    return inner

func = outter(3)
print(func(4))
print(func(4))

```

闭包和装饰器的区别
1. 闭包是函数，装饰器是特殊语法，在函数上使用`@`调用，使用方式不一样
2. 闭包的参数一般是变量，装饰器的参数一般是函数，装饰器是闭包的一种特殊应用
3. 闭包是为了保存某些中间值重复使用，装饰器是为了在代码上下增加新的功能，代码重复使用

## 上下文管理器

上下文管理器 (Context Manager) 用于某个对象或者函数在进入和退出规定的使用范围时，特殊的操作会被自动执行，一般是打开和关闭操作，如打开关闭文件，获取释放内存等。

一般的上下文管理器使用 `with ... as ...` 的形式，注册上下文管理器需要使用 `__enter__` 和 `__exit__` 方法，也可以使用内置函数 contextlib 。

装饰器也是在代码的上下增加新的功能，在一定程度下，闭包，装饰器，上下文管理器之间是可以相互转换的。

## Python 的默认参数陷阱

Python 中的函数在执行时，会根据编译好的函数体，命名空间和默认参数等新建一个函数对象，如果函数体未改变，那么每次调用函数执行的时候，函数的默认参数也是未改变的。

即 Python 函数的默认参数值，是在编译阶段就绑定的，函数的每次调用，默认参数并不会改变。

> Default values are computed once, then re-used.

即不仅是可变参数，不可变参数是不变的，只不过不可变参数未改变并不会有什么影响，而可变参数未改变则会造成影响，这种影响即有不好的地方，也有好的一面，比如用来做缓存。

## Python 字典 dict

Python 字典是一个键值映射关系的集合，底层实现是一个哈希表 (Hash Table) 。

字典是无序的，索引是对键的哈希，故字典中顺序不一定是写入的顺序，也不一定是按照键的大小顺序。

不，字典是完全无序的，并不是按照键值的哈希排序，字段的索引是完全无序的，和写入删除顺序也有关。所以同样的字典值，写入顺序不一样，使用 `dict.items()` 的的结果也是不一样的。

> [CPython implementation detail: Keys and values are listed in an arbitrary order which is non-random, varies across Python implementations, and depends on the dictionary’s history of insertions and deletions.](https://docs.python.org/2/library/stdtypes.html#dict.items)

但是字典可以保证，在没有其他操作的情况下,`dict.items()`  和 `item.keys()` 和 `item.values()`  的顺序是相同的。

因为需要对键值进行索引，所以并非所有的 Python 对象都可以作为键，只有可哈希的对象才能作为键值，即实现了 `__hash__` 方法的对象。 如不可变类型数字，字符串和元组可以作为键值，但是元组的元素必须为数字或者字符串，如果元组的元组有字典或者其他可变数据类型也不可以。

如果想要自己重载 `__hash__` 方法的话，注意返回值是 整型，而不是字符串。

但是在 Python 3.7 及以后，字典的哈希表修改了，在字典中是按照插入顺序存储。

> [Changed in version 3.7: Dictionary order is guaranteed to be insertion order.](https://docs.python.org/3/library/stdtypes.html#dict-views)

如果想使用按照写入的顺序存储的话，还可以使用 collections 里的 OrderDict

在 python3 中还有一个很大的修改，在 python2 中的 `dict.items()` 或者 `dict.keys()` 或者 `dict.items()` 得到的都是一个拷贝，是一个新建的对象。在生成对象之后，字典中的元素操作与它无关了。在 python3 中，这些方法得到的是一个动态指针，也是可以随着字典的值变化的。

## Python 列表 list

Python 列表是有序的序列容器，可以使用序号查找元素，可以使用分片切割列表。

列表可以进行直接乘法和加法运算。

可以直接创建列表，或者列表生成式创建列表，还可以使用列表迭代生成器创建列表。

在遍历列表或者创建列表的时候，可以使用迭代器减少内存消耗

列表无哈希方法，故不能作为字典的键，不能作为 set() 的元素。

## Python 元组 tuple

Python 元组是不可改变的序列容器，可以使用序号查找元素，可以使用切片切割元组，不能改变，增加和删除元素，可以联合，截取元组。

元组由于其特殊性，比列表占用内存更小，速度更快，可以作为字典的键。

## Python 集合 set

Python 集合是无序的，没有重复元素，元组不能通过序号查找。定义了集合的并交差等操作。

集合不能使用序号查找元素，只能使用 pop 获取元素，是无序的。使用 add 和 remove 增加删减元素。

如果想使用不可改变的集合，可以使用 frozenzet

快速创建列表 `[1,2,3]`，快速创建元组 `(1,2,3)`，快速创建集合 `{1,2,3}`

## python 中的与或非操作

python 中的与或非操作需要依靠 set 的并交叉集来完成

```
>>> a = [1,2,3]
>>> b=[3,4,5]
>>> list(set(a) & set(b))
[3]
>>> list(set(a).intersection(set(b)))
[3]
>>> list(set(a) | set(b))
[1, 2, 3, 4, 5]
>>> list(set(a).union(set(b)))
[1, 2, 3, 4, 5]
>>> list(set(a) ^ set(b))
[1, 2, 4, 5]
>>> list(set(a).symmetric_difference(set(b)))
[1, 2, 4, 5]
>>> list(set(a).difference(set(b)))
[1, 2]
```

## 可迭代对象和迭代器对象

可迭代对象不一定是迭代器对象，迭代器对象一定是可迭代对象。

可迭代对象需要实现 `__iter__` 方法或者 `__getitem__` 方法，迭代器对象除前面的之外，还需实现 `next` 或者 `__next__` 方法

## 类属性和实例属性

类属性为静态变量，故全局唯一，除非是一个常量或者十分清楚类属性，否则不要使用类属性

实例属性即每个实例唯一，修改实例的类属性不影响其他实例

类变量，其实更像是全局变量，一次定义，处处使用，全局唯一，不可乱用。

## py2 和 py3 的主要区别

1. `print` 由关键字变为函数
2. `xrange` 被取消合并入 `range`，`raw_input` 被取消合并入 `input`
> Python 3 中的 `range` 对象增加了 `__contains__` 方法，即可以使用 `in` 来做判断
3. 在代码中默认为 Unicode 编码，byte 类型和 str 类型被区分开，Unicode 类型和 str 类型合并，故 decode 和 encode 方法也被分开。
4. 迭代器对象的 `object.next()` 方法被取消合并入 `object.__next__()` 方法，函数 `next(object)` 继续保留
5. py2 中的 `/` 除数和被除数都为整数，结果为整数，否则结果为浮点数，`//` 结果下取整。py3 中的 `//` 结果为浮点数，`//` 结果下取整
6. 抛出异常和异常处理，py2 抛出异常`raise IOError, "file error"` 异常处理 `except NameError, err:`,py3 抛出异常`raise IOError("file error")` 异常处理 `except NameError as err:` .Python 2 兼容 Python 3.
7. 在 Python 2 中的全局变量和循环变量命名空间混淆，可能一个循环之后，全局变量 i 的值就不一样了， 在 Python 3.x 中 for 循环变量不会再导致命名空间泄漏。
> 列表推导不再支持 [... for var in item1, item2, ...] 这样的语法。使用 [... for var in (item1, item2, ...)] 代替。
8. 在 Python 2 中比较不可比较的类型时，如数组和字符串，竟然是可以比较的。Python 3 中的另外一个变化就是当对不可排序类型做比较的时候，会抛出一个类型错误。
9. `zip()`, `map()`, `filter()`, `dictionary's .keys()`, `dictionary's .values()`, `dictionary's .items()` 返回的是可以迭代器对象，而不是直接的列表。
10. python3 中没有 long 类型

判断 py2 还是 py3

```
# coding=utf-8

import sys

if sys.version_info[0] == 3:
    print('This is Python 3')
else:
    print('This is Python 2')

```

## Python 中单下划线和双下划线的作用

单下划线
1. 作为变量名
2. 在解释器中作为上一个语句执行的结果
3. 作为变量名前缀则为保护变量，在 `import *` 的场景下不会被引用，除非使用 `__all__` 包含改变量，或者引用时指明改变量

双下划綫
1. 作为变量名
2. 在对象内，作为变量名前缀则为私有变量，作为方法名前缀则为私有方法，除非使用 `_classname__spam` 才能找到 classname 为当前对象名，spam 为当前变量或者方法名
3. 前后都有双下划线，Python 惯例的特殊方法名，不建议在定义时使用这种格式

## HTTP 2.0

1. 单一长连接
2. 多路复用
3. 头部压缩
4. 二进制格式
5. 服务器端推送

## http 协议的连接状态

HTTP协议是无状态的和Connection: keep-alive是不一样的

无状态是指协议对于事务处理没有记忆能力，服务器不知道客户端是什么状态。从另一方面讲，打开一个服务器上的网页和你之前打开这个服务器上的网页之间没有任何联系。

HTTP是一个无状态的面向连接的协议，无状态不代表HTTP不能保持TCP连接，更不能代表HTTP使用的是UDP协议（面对无连接）。

从HTTP/1.1起，默认都开启了Keep-Alive保持连接特性，简单地说，当一个网页打开完成后，客户端和服务器之间用于传输HTTP数据的TCP连接不会关闭，如果客户端再次访问这个服务器上的网页，会继续使用这一条已经建立的TCP连接。

Keep-Alive不会永久保持连接，它有一个保持时间，可以在不同服务器软件（如Apache）中设置这个时间。


## 项目开发工作流程

开发模式 - 快速迭代开发， 开发流程 - gitflow 工作流

开发之前，先确定需求，评估项目可行性，对项目进行版本切分和开发任务划分。

开发时，主开发分支为 develop ，各自负责自己的部分，并新建自己的分支，有问题共同探讨，无问题则合并到 develop 分支。遇到新的需求，先等等，没准过几天就没了，真的需要也得加入到下一个开发版本。

完成开发版本，进入测试阶段，先进行项目的自测，测试驱动开发，使用现代的测试手段，如 nosetest ，pytest 等进行项目测试。

测试都完成之后，进入发版阶段 ，将 develop 分支合并到 release 分支，提供给客户端，或者其他的需求方，完成他们的部分。

在提交给其他部门之后，下一个版本的开发 feature 也要同步进行，如果其他部门遇到问题，则需在主开发分支 develop 上进行修复，修复完成后合并入 release 分支。

在各部门都完成开发测试工作之后，交给测试部门联合测试。继续进行下一版本的开发。

在测试部门测试无误通过后，正式上线，将 release 分支合并到 master 。将下一个版本的开发分支 feature 合并入主开发分支 develop。如果上线后遇到问题，则在 master 分支上做热修复 hot-fix 分支。


## 参考链接

[taizilongxu/interview_python](https://github.com/taizilongxu/interview_python)

[Python 2.7.x 和 Python 3.x 的主要区别](https://segmentfault.com/a/1190000000618286)

[acmerfight/insight_python](https://github.com/acmerfight/insight_python)

[Python 面试题集锦](https://michaelyou.github.io/2016/06/05/Python-%E9%9D%A2%E8%AF%95%E9%A2%98%E9%9B%86%E9%94%A6-%E8%BD%AC%E8%BD%BD/)
