---
layout: post
title: python 的未来
description: 夏虫不可语冰，我当然不是对 python 的未来发展指指点点，说三道四，而是说 python 中的 __future__
category: opinion
---

python2 和 python3 之间的巨大差异让这两者之间出现了不兼容性。python3 中有很多神奇的设计，python2 中的历史遗留问题不好处理，如何在 python2 中使用 python3 的神奇特性呢，不用写兼容代码，只需在文件开头引入 `__future__` 即可体会 python3 的魔力。

了解这些不同的特性，让我们对 python 2 和 python 3 的区别知晓的更多，也可以让我们对 python 的理解更进一步。

> `__future__` 引用必须在文件首部第一行


## Print

最有名的 python 2 和 python 3 的 `print` 是不一样的，python 2 中是关键字，而 python 3 中是函数。

在 python 2 中是支持 python 3 的打印方式的，但是 python 3 不支持 python 2 的方式。为了在 python 2 中强制使用 python 3 的打印方式，可以在文件首行引入 `print_function`

```
# -*- coding: utf-8 -*-
from __future__ import print_function

try:
    print "hello world"
except Exception as e:
    print(e)

```

结果是

```
  File "future_print.py", line 5
    print "hello world"
                      ^
SyntaxError: invalid syntax
```


## Unicode

在 python 2 和 python 3 中的 字符串是不一样的，具体可以看 [python3 中的编码和解码](https://windard.com/blog/2017/05/14/Python-Encode-And-Decode)

为了在 python 2 中体验 python 3 的字符串编码方式，可以在文件首行引入 `unicode_literals`

```
# -*- coding: utf-8 -*-
from __future__ import unicode_literals


print '\'xxx\' is unicode?', isinstance('xxx', unicode)
print 'u\'xxx\' is unicode?', isinstance(u'xxx', unicode)
print '\'xxx\' is str?', isinstance('xxx', str)
print 'b\'xxx\' is str?', isinstance(b'xxx', str)
```

结果是

```
'xxx' is unicode? True
u'xxx' is unicode? True
'xxx' is str? False
b'xxx' is str? True
```

## Division

在 python 2 中的除法默认是结果取整，如果想得到精确的结果需要使用 浮点数。而 python 3 则恰好相反，默认是获得精确结果。

为了在 python 2 中获得精确的除法结果，可以在文件首行引入 `division`

```
# -*- coding: utf-8 -*-
from __future__ import division

print 10 / 3
print 10 // 3
print 10.0 / 3
print 10.0 // 3

```

结果是

```
3.33333333333
3
3.33333333333
3.0
```

## Import

关于引用，我们先解释 python 中的两个概念
- module 库 ， 通常是单个的 python 文件
- package 包， 通常是整个文件目录，目录中必须含有 `__init__.py` 文件

假设有两个包，`pkg_demo` 和 `pkg_hope`

```
pkg_demo
├── __init__.py
├── mud_one.py
└── mud_two.py
pkg_hope
├── __init__.py
└── content.py
```

在同一个包中的两个库之间的相互引用，有以下几种方式

```
# -*- coding: utf-8 -*-
# from __future__ import absolute_import
# from mud_one import print_one
# from pkg_demo.mud_one import print_one
# from .mud_one import print_one

import string
# from . import string
from pkg_demo import string
# import mud_one
# from . import mud_one
# from pkg_demo import mud_one

# mud_one.print_one()
print string.letters

```

但是很奇怪，和网上看到的不一样、

关于 python 的包引用方式,python 2 中是相对路径引入，python 3 中是绝对路径引入。

```
Kopsoti
├── Klotski.py
├── __init__.py
└── builin.py
```

## Nested

## Generators

## With
