---
layout: post
title: Docker 的再次尝试
description: 可能是研究不深，并没有体验到 Docker 的便捷性，使用快速部署脚本或许也一样？
category: blog
---

互联网技术的发展迅猛，虚拟化技术已经十分成熟，常见的如个人 PC 上常用的各种虚拟机 VMware，VirtualBox 等，服务器上常见的Docker，Vagrant 等。

关于 Docker 和 Vagrant 的孰优孰劣不在这里探讨 ，Docker 的发展如火如荼，这里再写一点 Docker 的简单操作，如使用 Dockerfile 创建一个新的镜像，使用 Docker-compose 搭建 Docker 集群等。

Docker，Vagrant，VirtualBox，VMware 都曾在我的低端笔记本的垃圾 Windows 上试过，现在唯一还在使用的是 VMware 。

目前的开发环境也是在 VMware 中安装一个最小化的 Cent OS 7 ，不需要图形化界面，使用 ssh 连接进入，开启了 FTP 服务，配合使用 sublime 的 FTPSync 插件完美同步代码，彻底解决了开发环境与生产环境相差太大的问题，其实电脑里也已经装好了 Ubuntu 的双系统，但是还是觉得 Windows 好用一点。

这次的 Docker 尝试是在我本机上的 Cent OS 7 虚拟机中实现的，因为 Cent OS 的安全防护机制 SELinux ，导致有时会出现 权限问题，`permission denied`，建议关掉 SELinux ，因为我也不会配置。

临时关闭 SELinux `setenforce 0` ，或者使用特权模式运行 Docker `--privileged=true`，或者使用 `chcon `更改文件安全语境。

```
chcon -Rt svirt_sandbox_file_t /data/share/master #绝对路径
```

在国内使用默认的 Docker 源下载镜像比较慢，可以使用 DaoCloud, 阿里云等进行加速。

## Dockerfile

Dockerfile 是由一系列命令和参数构成的脚本，这些命令应用于基础镜像并最终创建一个新的镜像。

### 常用参数

```
FROM <image>:<tag>
```

指定基础 image，基础镜像可以是 Ubuntu 或者 cent OS 等这种按照 Linux 发行版本区分，也有 MySQL ， Nginx 等按照特定服务划分，或者docker 提供的一个最小的基础镜像 alpine ，还有他人制作发布的镜像，使用 Dockerfile 也就是为了制作一个 Docker 镜像。

指定镜像制作者信息。

```
MAINTAINER <name>
```

两种不同的写法，在镜像创建时所进行的操作。

```
RUN <command> (the command is run in a shell - `ls -al`)
RUN ["executable", "param1", "param2" ... ]  (commsnd split by space - `ls` `-al`)
```

从本地的文件系统中复制文件到镜像中

```
ADD <src> <dest>
```

用来设定环境变量，如 $PATH

```
ENV <key> <value>
```

持久化挂载，与文件复制不同，这是讲本地文件夹挂载到镜像中，实现文件的相互传输与共享。

```
VOLUME <src> <dest>
```

在镜像中切换目录，指定其为工作目录。

```
WORKDIR /path/to/workdir
```

指定向外暴露的的端口，在使用镜像时即可将容器中的端口映射到宿主机的端口。

```
EXPOSE <port> [<port>...]
```

设置启动容器的用户，默认为 root

```
USER <username>
```

类似于 RUN 命令，但是这个是在 镜像 启动时执行，如果有多条指令，则只指定最后一条，RUN 是有多条指定则全部执行。

```
CMD ["executable","param1","param2"] (like an exec, this is the preferred form)
CMD command param1 param2 (as a shell)
```

在 容器 启动时执行的命令，功能与 CMD 有部分的重合，同样的只有最后一条指定有效。

```
ENTRYPOINT ["executable", "param1", "param2"] (like an exec, the preferred form)
ENTRYPOINT command param1 param2 (as a shell)
```


### 使用 Dockerfile 创建一个 Python flask 镜像

app.py

```
# coding=utf-8

import os
from flask import Flask
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello():
    redis.incr('hits')
    return 'Hello %s! I have been seen %s times.' % (os.environ.get("ADMIN") or "world", redis.get('hits'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
```

Dockerfile

```
FROM python:2.7
ADD . /code
WORKDIR /code
ENV ADMIN windard
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python app.py
```

requirements.txt

```
flask
redis
```

三个文件都在同一目录下，现在开始构建镜像 (image)，并标记 (Tag)

目录结构

```
.
├── app.py
├── Dockerfile
└── requirements.txt
```

在当前目录下构建一个仓库为 `registry.cn-hangzhou.aliyuncs.com/windard/firsttry` ，Tag 为默认值 `latest` 的镜像。
因为制作镜像就是为了分发出去，如果你不通过网络分发，则 仓库名 可以随便取，如果通过网络分发，则需要按照分发商的仓库名书写，常见的 Docker 运营商有 Docker.io (官方 Docker 仓库), DaoCloud, Aliyun 等。

```
docker build -t registry.cn-hangzhou.aliyuncs.com/windard/firsttry .
```

这个是我在 阿里云 上新建的仓库地址，创建完毕后，即可认证关联阿里云账户上传镜像，然后就可以在阿里云的镜像仓库中下载我制作的镜像。

```
docker pull registry.cn-hangzhou.aliyuncs.com/windard/firsttry
```

使用 `docker images` 查看下载的镜像列表，使用 `docker rmi <imagesid>` 删除下载的镜像。

现在创建好了镜像，我们来开始使用这个镜像创建应用。

> 以上的步骤是创建并上传容器到云端，如果仅制作镜像，对镜像命名无需如此冗长 <br>
> 也可以直接使用已经运行的容器制作镜像 `docker commit –m 'add game 2048' 4807f56bb576 2048game` 镜像名即为 2048game

因为我们的容器中需要用到 redis ，所以先下载 redis 镜像，运行 redis 应用并命名为 redis_db。

```
docker pull redis
docker run -d --name redis_db redis
```

现在启动我们主要的 flask 容器,连接 redis_db 容器，设定环境变量 ADMIN，将我们的当前目录挂载到 `/code` 目录，这样就能实时更改代码。

```
docker run -d -p 5000:5000 --link redis_db:redis --name flasktest -e ADMIN=windard -v /root/Desktop/aliyun/docker:/code registry.cn-hangzhou.aliyuncs.com/windard/firsttry
```

现在访问我们的 `http://127.0.0.1:5000` 即可看到写入的环境和 redis 对每一个访问计数。

```
[root@localhost docker]# curl http://127.0.0.1:5000
Hello windard! I have been seen 1 times.
[root@localhost docker]# curl http://127.0.0.1:5000
Hello windard! I have been seen 2 times.
[root@localhost docker]# curl http://127.0.0.1:5000
Hello windard! I have been seen 3 times.
[root@localhost docker]#
```

如果更改代码的话也能会实时的显示出来，不仅因为将当前目录挂载，还因为我们的 flask 的也正处于调试模式，可以通过 `docker logs <containername>` 来查看详细日志。

这样启动我们的 docker 应用未免过于繁琐了一些，两个容器还需要分别启动然后创建连接。

我们可以将参数都写入到一个配置文件中，并使用配置文件启动 docker 应用，对关联的容器也自动启动，这就是 docker-compose。

## Docker-compose

安装 Docker-compose

```
sudo pip install -U docker-compose
```

然后我们来创建 `docker-compose.yaml` 配置文件在同一级目录下。

```
web:
    image: registry.cn-hangzhou.aliyuncs.com/windard/firsttry
    ports:
        - 5000:5000
    links:
        - redis
    volumes:
        - /root/Desktop/aliyun/docker:/code
    environment:
        - ADMIN=windard
redis:
    image: redis
```

启动 docker 容器中的 web 服务并后台运行，设定工程名为 flasktest。

```
docker-compose -p flasktest up -d web
```

docker-compose 不仅可以用来启动 docker 容器，还可以同时创建 docker 镜像。

```
web:
    build: .
    ports:
        - 5000:5000
    links:
        - redis
    volumes:
        - /root/Desktop/aliyun/docker:/code
    environment:
        - ADMIN=windard
redis:
    image: redis
```

这样就是在当前目录下创建镜像并启动容器。

关于 docker-compose 的配置信息，查看[官方文档](https://docs.docker.com/compose/compose-file/compose-file-v2/#service-configuration-reference)更简明易懂

- `docker-compose up -d` 后台运行当前目录下 `docker-compose.yml` 中的所有容器
- `docker-compose stop`  停止运行当前目录下 `docker-compose.yml` 中的所有容器
- `docker-compose build` 重新创建当前目录下 `docker-compose.yml` 中的镜像
- `docker-compose logs ` 查看容器日志，也可以指定容器名查看日志
- `docker-compose ps`    查看容器运行状态
- `docker-compose restart nginx` 仅重启 Nginx 容器


