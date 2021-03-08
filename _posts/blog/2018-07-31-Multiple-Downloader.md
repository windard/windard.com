---
layout: post
title: 多线程下载器
description: 面对中国的网速，不能吐槽。
category: blog
---

多线程下载器，常用的下载工具有 Chrome，wget，curl，种子下载器，迅雷等，能用，但总是觉得不够好用。

> 2021-03-08 填坑

## 前言
常见的下载场景，使用 curl,wget 一般也能够满足需求，在多线程下载的时候使用 axel 也可以做多线程下载，但是由于网络因素，或者重重原因，axel 也是偶尔抽风，下载超慢，不如自己动手，丰衣足食。

## filedown

使用 Python 实现的多线程下载器，开始使用的多线程，但是不好控制，后面改用线程池。

下载效果还可以，超时异常，失败重试，[GitHub 地址](https://github.com/windard/filedown)

已经上传到 pypi 源，可以直接安装使用,兼容 python2 和 python3.

```
pip install filedown
```

安装之后有两个下载命令，差异不大，一般使用后者。

```
$ filedown -h
Usage: filedown [OPTIONS] URL

Options:
  --thread / --process      Use ThreadPool or ProcessPool
  -w, --worker_num INTEGER  Number of workers
  -s, --chunk_size INTEGER  Chunk size of each piece
  -c, --timeout INTEGER     Timeout for chunk download
  -f, --filename TEXT       Filename of download
  -h, --headers TEXT        Headers to get file
  -c, --cookies TEXT        Cookie to get file
  -p, --proxies TEXT        Proxy to get file, pip install "requests[socks]"
  -h, --help                Show this message and exit.
$ concurrent_download -h
Usage: concurrent_download [OPTIONS] URL

Options:
  -h, --help             Show this message and exit.
  -n, --num INTEGER      thread number
  -c, --chunk INTEGER    chunk download size
  -t, --timeout INTEGER  chunk download timeout
```

## concurrent.download

使用 Java 实现的多线程下载器，同样是线程池实现，做的很简单。

[GitHub 地址](https://github.com/windard/concurrent.download)

使用 maven 导入

```
    <dependency>
        <groupId>com.windard.me</groupId>
        <artifactId>concurrent.download</artifactId>
        <version>1.1-SNAPSHOT</version>
    </dependency>
```

使用 jar 下载

```
$ java -jar concurrent.download-1.1-SNAPSHOT.jar
Usage: java -jar downloader.jar http://xxx.com/test.file
```

## godown

使用 Golang 实现，没想到 Golang 的性能这么好。

> GoDown: Goroutine Download For Golang

😂，所以名字里的 Go 并不是指 Golang，而是指 Goroutine。

实现了静态文件服务器和下载器的功能，还可以传入 URL 离线下载。

在下载器的部分，超时重试，使用 channel 做并发控制，保持 Goroutine 数量。

[GitHub 地址](https://github.com/windard/godown)

本人现在一般常用的也是这款，功能多样，性能强悍。

安装使用

```
go install github.com/windard/godown
```

使用命令

```
$ godown -h
NAME:
   GoDown - Goroutine Download For Golang

USAGE:
   godown [global options] command [command options] argument

VERSION:
   0.2.0

COMMANDS:
   download, d  download from server
   server, s    start static server
   help, h      Shows a list of commands or help for one command

GLOBAL OPTIONS:
   --help, -h     show help (default: false)
   --version, -v  print the version (default: false)
```
