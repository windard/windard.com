---
layout: post
title: Python 数组的遍历循环
category: project
description: Python 数组的遍历循环？还是循环遍历？
---

一个很简单的题目，在 [1,2,3,4,5] 中可以组成几个无重复数字的三位数。

显然 5*4*3 = 60 那么，如何在 Python 中把这 60 个数打印出来。

```
# coding=utf-8

import copy

digital = [1,2,3,4,5]

nums = []

for a in digital:
    digita = copy.copy(digital)
    digita.remove(a)
    for b in digita:
        digit = copy.copy(digita)
        digit.remove(b)
        for c in digit:
            nums.append(str(a)+str(b)+str(c))

print len(nums),nums
```

结果

```
60 ['123', '124', '125', '132', '134', '135', '142', '143', '145', '152', '153', '154', '213', '214', '215', '231', '234', '235', '241', '243', '245', '251', '253', '254', '312', '314', '315', '321', '324', '325', '341', '342', '345', '351', '352', '354', '412', '413', '415', '421', '423', '425', '431', '432', '435', '451', '452', '453', '512', '513', '514', '521', '523', '524', '531', '532', '534', '541', '542', '543']
```

或者一个看起来简单一些的写法

```
# coding=utf-8

import copy

m = copy.copy(digital)
n = [str(a)+str(b)+str(c) for a in m[:] for b in m[:] for c in m[:] if a!=b and b!=c and a!=c]

print len(n),n
```

结果是一样的，虽然这两种都能够得到答案，但是三位数就要三重循环，要是十位数就要十重循环，未免看起来不太好，或许可以迭代一下。

```
# coding=utf-8

import copy

digital = [1,2,3,4,5]
nums = []

def iteratool(n,a,size):
    if len(a)==size:
        nums.append(a)
        return
    for x in n :
        b = a
        b += str(x)
        m = copy.copy(n)
        m.remove(x)
        iteratool(m,b,size)
        if len(b)==size:
            b = b[:-1]

iteratool(digital,"",3)

print len(nums),nums
```

看起来正常了一点，但是当数据量增大的时候，迭代效率低，数据占据大量内存，应该可以用 yield 生成。可惜没有实现。

谁有更好的想法，可以一同交流。

这不就是全排列么。

在网上找到了一个函数可以做到。

```
# coding=utf-8

import itertools

digital = "12345"
nums = []

for item in itertools.permutations(digital,3):
    nums.append("".join(item))

print nums
```
 
以上排列相当于 A(5,3)=60，itertools 还可以算 C(5,3)=10 的操作，即相同的数字不同的组合算同一个。 

```
# coding=utf-8

import itertools

digital = "12345"
nums = []

for item in itertools.combinations(digital,3):
    nums.append("".join(item))

print nums
```