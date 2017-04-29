---
layout: post
title: Python 数组的遍历循环
category: project
description: Python 数组的遍历循环？还是循环遍历？
---

一个很简单的题目，在 [1,2,3,4,5] 中可以组成几个无重复数字的三位数。

显然 `5*4*3 = 60` 那么，如何在 Python 中把这 60 个数打印出来。

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

或者这样

```
# coding=utf-8

import copy

digital = [1,2,3,4,5]
nums = []

for a in digital:
    for b in digital:
        for c in digital:
            if (a!=b) and (b!=c) and (c!=a):
                nums.append(str(a)+str(b)+str(c))

print len(nums), nums
```

或者一个看起来简单一些的写法

```
# coding=utf-8

import copy

digital = [1,2,3,4,5]

n = [str(a)+str(b)+str(c) for a in digital for b in digital for c in digital if a!=b and b!=c and a!=c]

print len(n), n
```

结果是一样的，虽然这两种都能够得到答案，但是三位数就要三重循环，要是十位数就要十重循环，未免看起来不太好，或许可以迭代一下。

```
# coding=utf-8

import copy

digital = [1,2,3,4,5]
nums = []

def iteratool(digital, result, size):
    if len(result) == size:
        nums.append(result)
        return
    for x in digital:
        b = result
        b += str(x)
        m = copy.copy(digital)
        m.remove(x)
        iteratool(m, b, size)
        if len(b) == size:
            b = b[:-1]

iteratool(digital, '', 3)

print len(nums), nums
```

看起来正常了一点，但是当数据量增大的时候，迭代效率低，数据占据大量内存，应该可以用 yield 生成。可惜没有实现。

谁有更好的想法，可以一同交流。

这不就是排列组合么。

Python 的内置 itertools 库可以做到

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

在上面的排列组合问题中，如果只是排列，而且是全排列的话，有一个简单一点的算法

```
# coding=utf-8


def all_perms(elements):
    if len(elements) <= 1:
        yield elements
    else:
        for perm in all_perms(elements[1:]):
            for i in range(len(elements)):
                # nb elements[0:1] works in both string and list contexts
                yield perm[:i] + elements[0:1] + perm[i:]

print list(all_perms(range(3)))
print list(all_perms('abc'))

```

或者非要有选择的排列的话，itertools.permutations 的文档中列出了几种替代方法

```
# coding=utf-8


def permutations(iterable, r=None):
    # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) --> 012 021 102 120 201 210
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = range(n)
    cycles = range(n, n-r, -1)
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return

print len(list(permutations(xrange(10), 3)))
```

或者是是用 itertools.production

```
# coding=utf-8


from itertools import product


def permutations(iterable, r=None):
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    for indices in product(range(n), repeat=r):
        if len(set(indices)) == r:
            yield tuple(pool[i] for i in indices)

print len(list(permutations(xrange(10), 3)))

```

类似的，还有八皇后问题，我们先简化为三皇后问题，即在一个三乘三棋盘上，如何放置三个皇后棋子，使每个皇后水平或者垂直方向上都不会遇到其他皇后。

答案很简单，六种摆放方式。

```
# coding=utf-8

chess = [[0 for _ in xrange(3)] for _ in xrange(3)]

result = []

for a in xrange(3):
    for b in xrange(3):
        for c in xrange(3):
            if a!=b and b!=c and c!=a:
                result.append([a, b, c])

print len(result), result
```

或者这样

```
# coding=utf-8

import copy

chess = [[0 for _ in xrange(3)] for _ in xrange(3)]

result = []

def checkhorizontal(chess):
    for x in xrange(3):
        if sum(chess[x]) != 1:
            return False
    else:
        return True

def checkvertical(chess):
    for x in xrange(3):
        if sum([y[x] for y in chess]) != 1:
            return False
    else:
        return True

for a in xrange(3):
    for b in xrange(3):
        for c in xrange(3):
            subchess = copy.deepcopy(chess)
            subchess[0][a] = 1
            subchess[1][b] = 1
            subchess[2][c] = 1
            if checkhorizontal(subchess) and checkvertical(subchess):
                result.append([a, b, c])

print len(result), result
```

现在启用迭代

```
# coding=utf-8

result = []

import copy

def checkhorizontal(chess, size):
    for x in xrange(size):
        if sum(chess[x]) != 1:
            return False
    else:
        return True

def checkvertical(chess, size):
    for x in xrange(size):
        if sum([y[x] for y in chess]) != 1:
            return False
    else:
        return True

def solvequeen(chess, size, index):
    if index == size:
        if checkhorizontal(chess, size) and checkvertical(chess, size):
            result.append(chess)
        return
    for x in xrange(size):
        subchess = copy.deepcopy(chess)
        subchess[index][x] = 1
        solvequeen(subchess, size, index+1)

chess = [[0 for _ in xrange(3)] for _ in xrange(3)]

solvequeen(chess, 3, 0)

print len(result), result
```

这样的话，只需修改参数即可获得八皇后问题答案。

虽然这样确实可以得到，但是实际使用时发现确实太慢了。

而且，其实这还是排列组合问题的吖。

```
# coding=utf-8

result = []

import itertools

digital = xrange(8)

a = itertools.permutations(digital)

for item in a:
    result.append(item)

print len(result), result
```

这样就能很快的得出答案 40320。

。。。

但是我对八皇后的问题的理解有问题，不仅仅是不能在用一条直线上，在同一斜线上的也不可以，所以实际上八皇后的解只有 92 个。

```
# coding=utf-8

result = []

import copy

def checkhorizontal(chess, size):
    for x in xrange(size):
        if sum(chess[x]) != 1:
            return False
    else:
        return True

def checkvertical(chess, size):
    for x in xrange(size):
        if sum([y[x] for y in chess]) != 1:
            return False
    else:
        return True

def checkdiagonal(chess, size):
    points = []
    spaces = []
    for x in xrange(size):
        for y in xrange(size):
            if chess[x][y] == 1:
                points.append(x+y)
                spaces.append(x-y)
                break
    if len(set(points)) == len(points) and len(set(spaces)) == len(spaces):
        return True
    else:
        return False

def solvequeen(chess, size, index):
    if index == size:
        if checkhorizontal(chess, size) and checkvertical(chess, size) and checkdiagonal(chess, size):
            result.append(chess)
        return
    for x in xrange(size):
        subchess = copy.deepcopy(chess)
        subchess[index][x] = 1
        solvequeen(subchess, size, index+1)

chess = [[0 for _ in xrange(8)] for _ in xrange(8)]

solvequeen(chess, 8, 0)

print len(result)
```

这才是真正的八皇后问题，得到 92 个解，如果将旋转和对称的解归为一种的话，就是 12 个独立的解。

结果是 仍然非常慢，我们需要加速。

```
# coding=utf-8

import itertools 

result = []

def checkdiagonal(chessdot, size):
    points = []
    spaces = []
    for x,y in chessdot:
        points.append(x+y)
        spaces.append(x-y)
    if len(set(points)) == len(points) and len(set(spaces)) == len(spaces):
        return True
    else:
        return False

def solvequeen(size):
    for item in itertools.permutations(xrange(size)):
        chessdot = zip(xrange(size), item)
        if checkdiagonal(chessdot, size):
            result.append(chessdot)

solvequeen(8)

print len(result)
```

或者是强行压缩行数

```
# coding=utf-8

def solvequeen(size):
    return [chessdot for chessdot in __import__('itertools').permutations(xrange(size)) if len(set([i+chessdot[i] for i in xrange(size)])) == len([i+chessdot[i] for i in xrange(size)]) and len(set([i-chessdot[i] for i in xrange(size)])) == len([i-chessdot[i] for i in xrange(size)]) ]

print len(solvequeen(8))
```

再次压缩版

```
# coding=utf-8

def solvequeen(size):
    return [chessdot for chessdot in __import__('itertools').permutations(xrange(size)) if len(set([i+chessdot[i] for i in xrange(size)])) == size == len(set([i-chessdot[i] for i in xrange(size)]))]

print len(solvequeen(8))
```

在 八皇后问题 一开始的思路是先确定八个皇后的位置，然后判断当前这个位置状态是否符合，如果不符合则舍弃，否则标记保留下来。

但是这个方法有一个很大的问题，就是需要遍历所有的可能的情况。

在三皇后问题上还可以遍历，但是八皇后问题则需要遍历 `8**8 = 16777216` 一千六百多万种情况，所以就会非常慢。

现在我们换一个思路，能不能先确定一个皇后的位置，然后在选择下一个皇后的位置的时候判断这个皇后的位置是否不与之前的皇后的位置冲突，这样就能大大的节省时间。

```
# coding=utf-8

result = []
state = []

def conflict(state, point):
    num = len(state)
    for x in xrange(num):
        if abs(state[x] - point) in (0, num-x):
            return True
    return False

def solvequeen(size, state, index):
    if index == size:
        result.append(state)
        return
    for x in xrange(size):
        if not conflict(state, x):
            substate = state[:]
            substate.append(x)
            solvequeen(size, substate, index+1)

solvequeen(8, state, 0)

print len(result)

```

或者这样

```
# coding=utf-8

def conflict(state, point):
    num = len(state)
    for x in xrange(num):
        if abs(state[x] - point) in (0, num-x):
            return True
    return False

def queens(num, state):
    for pos in xrange(num):
        if not conflict(state, pos):
            if len(state) == num-1:
                yield (pos, )
            else:
                for result in queens(num, state+(pos, )):
                    yield (pos, ) + result

q = queens(8, ())
result = []

while 1:
    try:
        result.append(q.next())
    except:
        break

print len(result)
```

附上一个 C语言版的 八皇后问题

```
#include<stdio.h>

#define Queens 8 /*皇后数量*/
#define Output 1 /*(Output=0 or 1)，Output用于选择是否输出具体解,为1输出，为0不输出*/

int A[Queens*3], B[Queens*3], C[Queens*3], k[Queens+1][Queens+1];
int inc, *a=&A[Queens], *b=&B[Queens], *c=&C[Queens];

void lay(int i)
{
    int j=0, t, u;
    while(++j<=Queens)
    if(a[j]+b[j-i]+c[j+i]==0)
    {
        k[i][j]=a[j]=b[j-i]=c[j+i]=1;
        if(i<Queens)lay(i+1);
        else
        {
            ++inc;
            if(Output)
            {
                for(printf("(%d)\n",inc),u=Queens+1; --u; printf("\n"))
                    for(t=Queens+1; --t;)k[t][u]?printf("Q "):printf("+ ");
                printf("\n\n\n");
            }
        }
        a[j]=b[j-i]=c[j+i]=k[i][j]=0;
    }
}
int main(void)
{
    lay(1);
    printf("%d皇后共计%d个解",Queens,inc);
    getchar();
    return 0;
}
```

最后以一个一行代码实现的八皇后问题的解来结束

```
_=[__import__('sys').stdout.write("\n".join('.' * i + 'Q' + '.' * (8-i-1) for i in vec) + "\n===\n") for vec in __import__('itertools').permutations(xrange(8)) if 8 == len(set(vec[i]+i for i in xrange(8))) == len(set(vec[i]-i for i in xrange(8)))]
```