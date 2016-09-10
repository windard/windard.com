---
layout: post
title: python中的不换行输出
category: project
description: Python的print输出是默认换行的，那么，怎样才能不换行输出呢？
---

在Python中实现换行，我本来以为只是一件小事情，结果发现没那么简单。    

#### Python 2.X
1. print后加上`,`
```python
for i in range(100):
	if i%10==0 and i!=0:
		print "\n"
	print i,
```

![line_break_2_1.jpg](/images/line_break_2_1.jpg) 

> 注意，虽然没有换行，但是在两次输出之间还是默认有一定的距离。

2. 使用`sys.stdout.write()`。当然你得先引入sys这个库，而且有时候需要在这个后面加上`sys.stdio.flush()`，不然可能因为在缓存区里看不见。 

```python
import sys
for i in range(100):
	if i%10==0:
		print "\n"
	sys.stdout.write(str(i)+" ")
```

![line_break_2_1_2.jpg](/images/line_break_2_1_2.jpg)
> 注意，打印的参数只能是字符串或者是数组。

#### Python 3.X
1. print()的原型是`print(*objects,sep='',end='\n',file=sys.stdout,flush=False)`，所以只需要将`end='\n'`给替换掉就可以了。    

```python
for i in range(100):
	if i%10==0:
		print("")
	print(i,end=" ")
```

![line_break_3_1.jpg](/images/line_break_3_1.jpg)
 
2. 也是使用`sys.stdout.write`         

```python
import sys
for i in range(100):
	if i%10==0 and i!=0:
		print("")
	sys.stdout.write(str(i)+" ")
```
 
![line_break_3_2.jpg](/images/line_break_3_2.jpg)