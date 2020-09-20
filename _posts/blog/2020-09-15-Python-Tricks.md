---
layout: post
title: Python Tricks
description: 一些 Python 使用的小技巧
category: blog
---


熟练使用可以让你的代码更简洁，避免使用也能让你跳过很多坑

---

### 变量互换

```bash
>>> a,b = 1,2
>>> a,b
(1, 2)
>>> a,b = b,a
>>> a,b
(2, 1)
```
---

### 元素还是元组

```python
a = 1
b = 2,
print(a)
print(b)

c = (1 )
d = (1, 2)
print(c)
print(d)

e = 2,
f = 2, 3
g = 2, 3, 4
print(e)
print(f)
print(g)
```

---

### 神出鬼没的逗号

```python
print("hello " "world")
print(
    'cccccccc' in ['aaaaaaaa', 'bbbbbbbb', 'cccccccc' 'dddddddd', 'eeeeeeee',]
)

print("hello " 
      "world")
print(
    'cccccccc' in ['aaaaaaaa', 'bbbbbbbb', 'cccccccc' 
                   'dddddddd', 'eeeeeeee',]
)
```

---

### 无异常的结束

```python
def else_in_loop():
    for i in range(10):
        print i
        # break
    else:
        print("no break in loop")

    # or
    
    while False:
        pass
    else:
        print("no break in loop")


def else_in_except():
    try:
        1 / 0
    except ZeroDivisionError:
        pass
    else:
        print("no exception in exception handling")
```

---

### 逻辑运算符

```python
def check_path(req):
    if req:
        if req.biz:
            if req.biz.path:
                return req.biz.path

    # return req and req.biz and req.biz.path


def get_first(a, b, c):
    if a:
        return a
    if b:
        return b
    if c:
        return c

    # return a or b or c


if __name__ == '__main__':
    print(1 and 2 and 3)
    print(1 or 2 or 3)
    print(0 and 1 and 2)
    print(0 or 1 or 2)

```
短路计算

---

### 默认参数陷阱

```python
def foo(x=[]):
    x.append(1)
    print x

if __name__ == '__main__':
    foo()
    foo()
    foo()
    foo()

# [1]
# [1, 1]
# [1, 1, 1]
# [1, 1, 1, 1]
```

--- 
### 变量泄露

```python
# fixed in python3

i = 10
a = [i for i in range(5)]
print(i)



最终的返回
# same with java

def main():
    try:
        return 1
    except:
        return 2
    finally:
        return 3
```

---

### 禅

```sh
>>> import this
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
