---
layout: post
title: 鸭子模型
category: project
description: 如果它走路像鸭子，叫声也像鸭子，我们就认为它是鸭子。
---

鸭子模型在 python 中用的很多，主要是在类文件 file 对象的使用中。

鸭子模型就是说 `当看到一只鸟走起来像鸭子、游泳起来像鸭子、叫起来也像鸭子，那么这只鸟就可以被称为鸭子。` 而类文件对象主要的两个方法就是 write() read() 和 close() ，也就是说只要一个类有这样的几种方法就可以被称为类 file 类。

一直不太理解鸭子模型，终于在这次遇到了。

python 的 logging 模块，是一个用来输出 log 的模块，平常使用的时候主要使用它的前两个类，将 log 输出到文件或屏幕上，但是现在我需要获得它的 log ，通过图形化界面输出出来，但是它只有输出到流的几个子类， logging 的子类如下。

|子类                 |功能                                                                                                             |
|---                    | ---                                                                                                               |
|StreamHandler      |发送错误到流(类似文件的对象)。|
|FileHandler        |发送错误到磁盘文件。|
|BaseRotatingHandler|是所有轮徇日志的基类，不能直接使用。但是可以使用RotatingFileHandler和TimeRotatingFileHandler。|
|RotatingFileHandler    |发送信息到磁盘文件，并且限制最大的日志文件大小，并适时轮徇。|
|TimeRotatingFileHandler    |发送错误信息到磁盘，并在适当的事件间隔进行轮徇。|
|SocketHandler  |发送日志到TCP/IP socket。|
|DatagramHandler    |发送错误信息通过UDP协议。|
|SMTPHandler    |发送错误信息到特定的email地址。|
|SysLogHandler  |发送日志到UNIX syslog服务，并支持远程syslog服务。|
|NTEventLogHandler  |发送日志到WindowsNT/2000/XP事件日志。|
|MemoryHandler  |发送日志到内存中的缓冲区，并在达到特定条件时清空。|
|HTTPHandler    | 发送错误信息到HTTP服务器，通过GET或POST方法。|

看到第一个的 StreamHandler 可以用类文件对象，可是还是不太清楚，看一下官方文档，对这个类的描述的是
`StreamHandler类位于核心logging包，将日志输出发送至如sys.stdout, sys.stderr这样的流对象，或者任何的类文件对象（更准确的说，支持 write() 和 flush() 方法的对象）。`

这样的话，就很清楚的了，让我来实现一个类文件对象看能不能用。

```
#coding=utf-8
import sys
import logging
from PyQt4 import QtGui,QtCore

logger = logging.getLogger("Duck Logging")
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(lineno)-4d %(message)s', '%a, %d %b %Y %H:%M:%S',)

class DuckLog(object):
    """Duck Log"""
    def __init__(self):
        self.name = "Duck Log"
        self.content = ""

    def write(self,content):
        self.content += content

    def read(self):
        return self.content

    def close(self):
        pass

    def flush(self):
        pass

log = DuckLog()

log_handler = logging.StreamHandler(log)
log_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(log_handler)

logger.setLevel(logging.DEBUG)

logger.info("Hello")

logger.error("WHAT FUCK")

logger.warning("WARNING")

print "Duck Log"
print log.read()

```

执行输出结果为

```
Duck Logging Sat, 18 Jun 2016 20:43:38 INFO     293  Hello
Duck Logging Sat, 18 Jun 2016 20:43:38 ERROR    295  WHAT FUCK
Duck Logging Sat, 18 Jun 2016 20:43:38 WARNING  297  WARNING
Duck Log
Duck Logging Sat, 18 Jun 2016 20:43:38 INFO     293  Hello
Duck Logging Sat, 18 Jun 2016 20:43:38 ERROR    295  WHAT FUCK
Duck Logging Sat, 18 Jun 2016 20:43:38 WARNING  297  WARNING

```

就是这样。
