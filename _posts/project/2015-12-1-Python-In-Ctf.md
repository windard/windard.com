---
layout: post
title: 用Python解决ctf中常见的栅栏密码和凯撒密码
category: project
description: 本人ctf新手，大牛勿见笑。
---

事情的缘由是最近做了几场ctf比赛，看到有凯撒密码和栅栏密码，便用Python尝试了一下，发现还是蛮好使的，无所不能的Python。   

####IDF实验室--聪明的小羊  

```
一只小羊跳过了栅栏，两只小样跳过了栅栏，一坨小羊跳过了栅栏...

tn c0afsiwal kes,hwit1r  g,npt  ttessfu}ua u  hmqik e {m,  n huiouosarwCniibecesnren.
```

这道题目已经明显的提示了是栅栏密码的题目，关于栅栏密码可以看[这里](http://baike.baidu.com/link?url=xuEPgV8vKEU6VyZNy2dGvheehY4NBI21cVkUl6wzJNYv269tQpncGlC_5EiqlnOK1R_JqJQg1tc-Hu9i4c9Tu_)。                 
大体思路就是将你的明文按行排列起来，然后按列读取密文，就像明文`Baby,I Love You Forever!`,按两行排列起来就是：                   

```
Baby,I Love 
You Forever!
```

所以从上往下一列一列的读取就是`BYaobuy ,FIo rLeovveer !`。          
这样的密文拿到之后我们先找到它的所有公因数，然后分别按它的公因数排成相应的行数，找到其中的一个最有意义的就是明文了。       
不过如果仅是这样的话，那么有什么样的结果害的靠眼睛来寻找就太慢了，如果是在ctf比赛中，一般的flag都是有一定的规格的，比如说XXXX{}，那么，我们只要找到了XXXX就可以判断这个就是明文了。          
按照这样的思路，在idf中的flag一般是wctf{XXXX}，所以我们找到wctf即可，代码如下：

```python
#coding=utf-8
data1 = "tn c0afsiwal kes,hwit1r  g,npt  ttessfu}ua u  hmqik e {m,  n huiouosarwCniibecesnren."
length =  len(data1)
for i in xrange(2,length):
	if length%i==0:
		s = ""
		for j in range(i):
			for m in range(j,length,i):
				s = s+data1[m]
		if "wctf" in s:
			print s
```

结果是`the anwser is wctf{C01umnar},if u is a big new,u can help us think more question,tks`.

####ZJPC-CTF
也是一道栅栏密码的题目，密文如下。
```
T IFCCH NONY AZCA_N_PRHRLEEIEIF CPFGJ{IFCCH!EA N PRSUTERTL.PRLEEIE}
```
但是这道题就非常坑爹了，它一共是67个字符，没有公因数，那么我们要删掉一定的空格或者全部的空格才可以了。               
那没有办法，我们就只能先分别删掉它的每一个空格使其为66位，然后再来找了。        

```python
#coding=utf-8

def deletespace(data):
	s = data.split(" ")
	m = []
	for i in range(1,len(s)):
		l = ""
		for j in range(len(s)):
			if j==i:
				l = l+s[j]
			else:	
				l = l+" "+s[j]
		l = l.strip()
		m.append(l)
	return m

data = "T IFCCH NONY AZCA_N_PRHRLEEIEIF CPFGJ{IFCCH!EA N PRSUTERTL.PRLEEIE}"
d = deletespace(data)
for data1 in d:
	length =  len(data1)
	for i in xrange(2,length):
		if length%i==0:
			s = ""
			for j in range(i):
				for m in range(j,length,i):
					s = s+data1[m]
			if "ZJPC" in s:
				print s
```
结果竟然跑出来两个，还好答案只有一个。              
```
THE RAILNFE CEPCIRHES IUNFTO ENCRYPT FLAG.ZJPC{RAIL_FENCE_CIPHER!}
THE RAIL FENCEPCIRHES IUNFTO ENCRYPT FLAG.ZJPC{RAIL_FENCE_CIPHER!}
```

####ZJPC-CTF
凯撒密码                        
```
AKQD{dbftbs_jt_hppe_cvu_Xfbl!}
```
凯撒密码源于古罗马帝王凯撒，因为他当年想出了这种加密方式，故一次命名，关于凯撒密码可以看[这里](http://baike.baidu.com/link?url=1bv7dK0yEukVC40yxTWE2G3XbqYUuhzeA-fuSbH-pLqV5k6pva-siRyNAKk4fKTK11ahY9YEmT0lWSougOKbVCicP5u3Fi69tHk6x0LPl9OAaIgAdVN6TykTyFS5dDMc2TGFroeuZKHtms0pkDTCieYm8kCtoQLs9uNx3anT001NS1xVLiGdfksQjwyFMTfZ)。
原理也很简单，就是按照26个英文字母的顺序分别用这个字符的前面或者后面第多少位来替换，做如下对应。   
```
ABCDEFGHIJKLMNOPQRSTUVWXYZ    abcdefghijklmnopqrstuvwxyz
DEFGHIJKLMNOPQRSTUVWXYZABC    defghijklmnopqrstuvwxyzabc
```
那么还是原来的那个例子,明文`Baby,I Love You Forever!`，那么密文就是`Edeb,L Oryh Vrx Iruhyhu!`。  
这样的话，拿到了密文之后，我们分别将它的每一个字符进行移位，找到最有意义的那个就是flag了，当然，在这里，我们也需要用有没有flag特定的字符来判断是不是找到了真正的flag。          
按照上面的思路，但是这里有两个地方有点困难，就是特殊标记不予替换和替换超长轮回，代码如下：        

```python
#coding=utf-8

def ischar(i):
	if i>='a' and i<='z':
		return 1
	elif i>='A' and i<='Z':
		return 2
	else:
		return 0

def litcha(j,i):
	if chr(ord(j)+i)>'z':
		return chr(ord('a')+ord(j)+i-ord('z')-1)
	else:
		return chr(ord(j)+i)

def bigcha(j,i):
	if chr(ord(j)+i)>'Z':
		return chr(ord('A')+ord(j)+i-ord('Z')-1)
	else:
		return chr(ord(j)+i)

data = "AKQD{dbftbs_jt_hppe_cvu_Xfbl!}"
for i in range(26):
	data1 = ""
	for j in data:
		if ischar(j)==1:
			j = litcha(j,i)
		elif ischar(j)==2:
			j = bigcha(j,i)
		else:
			pass
		data1 = data1+j
	if "ZJPC" in data1:
		print data1

```

显得稍微复杂了一点，不过结果还是成功出来了，明文是`ZJPC{caesar_is_good_but_Weak!}`，凯撒密码的保护能力有限，也就这样了。      

####ZJPC-CTF
凯撒密码的加强版。   
```        
Task:
I guess you are done with Caesar, aren't you?
The big problem with caesar is that it does not allow digits or other characters.
I have fixed this, and now I can use any ascii character in the plaintext.
The keyspace has increased from 26 to 128 too. \o/


37 23 32 33 38 23 25 30 30 33 3b 
23 28 2d 2b 2d 38 37 23 33 36 23 
33 38 2c 29 36 23 27 2c 25 36 25 
27 38 29 36 37 0d 23 2c 25 3a 29 
23 2a 2d 3c 29 28 23 38 2c 2d 37 
23 25 32 28 23 32 33 3b 23 0d 23 
27 25 32 23 39 37 29 23 25 32 3d 
23 25 37 27 2d 2d 23 27 2c 25 36 
25 27 38 29 36 23 2d 32 23 38 2c 
29 23 34 30 25 2d 32 38 29 3c 38 
2a 30 25 2b 1e 0e 14 07 3f 3d 33 
39 23 36 23 3b 2d 32 41 

```
看着这些数字，猜测应该是十六进制，题目中也提示了，凯撒密码从单纯的英文字母转到了128的ASCII码，好吧，其实是更简单了好么。。。               
先将十六进制转换为ASCII码，然后分别替换，代码如下：
```python
#coding=utf-8

data = """
37 23 32 33 38 23 25 30 30 33 3b 
23 28 2d 2b 2d 38 37 23 33 36 23 
33 38 2c 29 36 23 27 2c 25 36 25 
27 38 29 36 37 0d 23 2c 25 3a 29 
23 2a 2d 3c 29 28 23 38 2c 2d 37 
23 25 32 28 23 32 33 3b 23 0d 23 
27 25 32 23 39 37 29 23 25 32 3d 
23 25 37 27 2d 2d 23 27 2c 25 36 
25 27 38 29 36 23 2d 32 23 38 2c 
29 23 34 30 25 2d 32 38 29 3c 38 
2a 30 25 2b 1e 0e 14 07 3f 3d 33 
39 23 36 23 3b 2d 32 41 
"""

data1 = data.replace(" ","")
data2 = data1.replace("\n","")
data3 = data2.decode("hex")

def chang(j,i):
	if ord(j)+i >=128:
		return chr(ord(j)+i-128)
	else:
		return chr(ord(j)+i)
	
for i in range(128):
	l = ""
	for j in data3:
		j = chang(j,i)
		l = l+j
	if "ZJPC" in l:
		print l
```

好了，大概就讲这么多了，这道题的结果是`s_not_allow_digits_or_other_charactersI_have_fixed_this_and_now_I_can_use_any_ascii_character_in_the_plaintextflagZJPC{you_r_win}`。        

Python 无所不能。