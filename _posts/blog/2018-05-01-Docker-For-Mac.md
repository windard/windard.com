---
layout: post
title: Docker for Mac 的网络问题
description: Docker 的网络拓扑研究
category: blog
---

## Docker

Docker 作为新一代的虚拟机软件,极大的增强了虚拟机使用的简易性和灵活性。通过容器服务，来创建新的虚拟机来进行开发部署。

## Docker 在 Mac 上的演进

因为 Docker 的后台程序使用了 Linux 特有的内核特性，所以不能在 Mac 或者 Windows 平台上直接使用 Docker。

所以在开始的时候使用的是 docker-machine (包含于 Docker Toolbox) 来创建一个 Linux 虚拟机，然后在这台虚拟机上使用 Docker。

一个标准的 Docker 程序都是由三部分组成的

- Docker client: 连接 docker 后台进程，提供 docker 操作命令
- Docker daemon: docker 后台进程，管理容器 container （docker client 和 docker machine 是通过 restful API 交互的，所以理论上，也可以自行构造客户端甚至使用 curl 交互）
- container: Docker 运行的容器

在 Linux 上这三者的架构图
![/images/linux_docker_host](/images/linux_docker_host.svg)

而在 Mac 下则由 client 连接 Linux 中的 Docker 后台程序
![mac_docker_host](/images/mac_docker_host.svg)

所以以前在 Mac 上使用 docker 时，需要使用 `docker-machine create default` 来首先创建一个 Linux 虚拟机。docker-machine 默认使用的 virtualbox 创建虚拟机，如果之前已有安装过 virtualbox，需要先将其关闭，在 docker toolbox 中包含有 virtualbox

> 不过 docker-machine 也支持使用其他驱动来创建虚拟机，比如 xhyve

创建之后将 default 虚拟机设定为 docker daemon，然后就可以正常使用 docker 命令来使用 docker 操作了。

```
docker-machine create -d virtualbox default
docker-machine env default
eval "$(docker-machine env default)"
docker info
```

使用 `docker-machine ls` 查看 virtualbox 创建的虚拟机。
使用 `docker ps` 查看 docker 创建的虚拟机容器。
使用 `docker-machine ip default` 查看虚拟机的 IP

在这种方式下启动的 docker 容器，实际上是启动在 Linux 服务器中，端口映射也不能直接到 Mac 主机上，而是在 default 的虚拟机上，所以需要通过 default 主机的域名和端口去访问容器内的服务。

主机和容器之间还有一层 Linux，通过桥接网络连接。

所以在 Mac 上现在推荐使用的 Docker for Mac。Docker for Mac 使用的是 Mac 自己的虚拟服务 HyperKit 而不是 virtualbox 创建虚拟机，无需手动再创建 default Linux 虚拟机。

现在无论使用 `brew install docker` 或者是下载 dmg 文件手动安装，都是使用 Docker for Mac。

使用 Docker for Mac 之后，容器的端口映射直接在本机上，可以使用 localhost 或者 127.0.0.1 的域名访问到。

## 主机与容器的相互访问

在 Docker for Mac 中，是不能从主机直接访问容器 IP 的，只能通过端口映射来访问容器的服务。

在容器中可以访问到主机和其他容器，可以在 Docker for Mac 的配置中找到网关的地址，即时主机的地址，或者使用 `docker.for.mac.localhost` 来代替主机的地址。

所以总结就是在 Mac 上，使用 Docker for Mac 是无法访问到容器的 IP 的，但是可以在容器内访问主机，如果想要主机访问容器，只能通过端口映射的方式访问其服务。


## 存储位置

在 docker for Mac 中，所有的 images 都存储在以下文件中

```
/Users/{YourUserName}/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux/Docker.qcow2
```

## 参考文档

[Docker for Mac vs. Docker Toolbox](https://docs.docker.com/docker-for-mac/docker-toolbox/)

[Networking features in Docker for Mac](https://docs.docker.com/docker-for-mac/networking/#httphttps-proxy-support)

[Docker - 从入门到实践](https://yeasy.gitbooks.io/docker_practice/content/introduction/)
