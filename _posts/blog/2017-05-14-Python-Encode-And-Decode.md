---
layout: post
title: python3 中的编码和解码
description: 在 Python 2 中的对中文编码和解码问题就已经令人头疼了，在 Python 3 中字符串全部采用 Unicode 编码，没想到又到了另一种编码和解码问题中。
category: blog
---

在 Python 2 中的 str 和 Unicode 傻傻分不清，如果还不幸在 Windows 平台下，那简直是一场灾难。在 Python 3 中这种情况大为好转， str 默认是 Unicode 编码，但是又出现了另一个问题。在 Python 2 中 bytes 和 str 是隐式相同的，在 Python 3 中它们被严格区分开。

世界上最幸福的 Python 程序员是在 Mac 上写 Python 3 ，最不幸的 Python 程序员是在 Windows 下写 Python 2。

为了更好的与 Python 2 的对比，本文在 Ubuntu 下进行，字符串都是指中文字符串。

## bytes/str

字节流和字符串，前者表示二进制数据，后者表示文本，在 Python 3 中所有的网络协议中使用的都是 bytes 。

在 Python 2 中这两者是可以混用的，但是在 Python 3 中则不能，这表示你不能拼接 bytes 和 str ，不能在 bytes 中查找 str， 不能在 str 中查找 bytes。

bytes 和 str 的联系是 bytes 解码(decode)为 str, str 编码(encode)为 bytes。

所以 bytes 只有 decode 函数，而无 encode 函数，str 只有 encode 函数，而无 decode 函数。

因为在 Python 3 中所有的字符串都是 Unicode 格式，采用 utf-8 编码，所以默认的编码和解码都是默认采用 utf-8 格式。

![python3](/images/python3.png)

## str/unicode

不要忘了 Python 2 中文编码带来的恐怖。

字符串和万国码，在 Python 3 中这两者是一致的，但是在 Python 2 中，因为 Python 2 的推出比万国码的推出更早，所以在 Python 2 中这两者是不同的。

不过在 Python 2 中字符串和字节流是相同的。

在 Python 2 中字符串和万国码不能混用，这表示不能拼接 Unicode 和 str，不能在 Unicode 中查找 str，不能在 str 中查找 Unicode。

Unicode 和 str 的联系是 Unicode 编码(encode)为 str, str 解码(decode)为 Unicode。

所以 Unicode 编码为 str 之后不能再次编码，str 解码为 Unicode 之后，不能再次解码。

![python2](/images/python2.png)

在 Python 2 中没有默认的解码和编码方式，故解码和编码都要声明是 utf-8。

## unicode/gbk

虽然不想说，但是还是要面对，目前市场份额最大的 Windows 。

Windows 的中文默认编码为 gbk，虽然它有很多名字 gb2312，gbk，chap 936，但这些都是一路货色，不与 Unicode 相同。

Python 2 中的除 ASCII 之外字符，采用与本机编码相同的编码格式，所以在 Windows 下就是采用 gbk 编码。

字符串默认采用 gbk 编码，所以在 Windows 下的话，字符串其实 gbk 字符串，在与 Unicode 字符串的转换中就更多了一步。

![windows](/images/windows.png)

## utf-8/gbk

在 Python 3 中，已经不论是在什么平台下都是采用 Unicode 编码格式，可以编码为 bytes 格式，然后解码，也可以编码为 gbk 格式，然后解码。这才是正确的方式。

utf-8 与 gbk 是同一等级的，两者只是不同的编码方式，utf-8 中将每个字符串编码为 3 个字节，而 gbk 中将每个字符串编码为 2 个字节。

Unicode 与 ASCII 与 gbk 也是同一个等级的，三者是对不同的文字有不同的表示，ASCII 中每个文字一个字节，才能表示西文字母和数字等，不能表示中文，gbk 中每个文字两个字节，可以表示汉字，Unicode 中每个文字一个 Unicode 单位，字节数的话由编码方式来决定，utf-8 是变长的编码方式，中文是三个字节长，范围在 \u4e00-\u9fa5 之间。

![perfect](/images/perfect.png)

## 总结

在 Python 2 中，字符串和字节流是相亲相爱的一家人，Unicode 是标准，字符串转化为 Unicode 需要解码，Unicode 转换为字符串需要编码。

在 Python 3 中，字符串和 Unicode 是一家人，而且还是标准，字节流转换为字符串需要解码，字符串转化为字节流需要编码。

在写入到文件中时，除非使用二进制格式打开，否则都是只能写入字符串，所以在 Python 2 中由 Unicode 编码为字符串，在 Python 3 中由字节流解码为字符串 (Unicode) 。

在网络文件接收到的数据，一般都是采用 Unicode 格式编辑，在 Python 2 中可以由字符串解码为 Unicode ，在 Python 3 中可以由字节流解码为 Unicode (字符串)。
