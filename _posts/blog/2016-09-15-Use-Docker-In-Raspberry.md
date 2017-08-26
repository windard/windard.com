---
layout: post
title: 在树莓派上使用 Docker
description: Docker Is The Future
category: blog
---

## 安装 Docker

Dell Inspiron 14 + Windows10 && 树莓派一代B+ + raspbian 4.10

在树莓派的比较新的版本里官方源中 `Docker` ， 可以通过 `sudo apt-get install docker.io `下载，对的，它在源里并不叫 `docker` ，因为已经有一个文件系统应用叫 `docker`,但是我的 `树莓派二代B` 的源里并没有 `Docker` ，不知道为什么，可以通过 `sudo apt-cache search docker` 来查看自己的源里有没有 `Docker`

然后我就想在官网下下载二进制软件安装，可惜需要 `Linux` 3.10 及以上的内核，可以通过 `file /sbin/init` 查看内核版本，我的内核版本是 2.6.6 ，并不能安装。

在此处就曾想过算了，于是想在 Windows 上试一下 Docker 好了，下载了 Docker 安装包结果需要 `Hyper-V` 的支持，并不知道这个是什么，于是安装 Docker-Toolbox ，跟 Docker 一样的，安装好之后桌面上出现三个新的图标 `Docker Quickstart Terminal` , `Kitematic (Alpha)` 和 `Oracle VM VirtualBox` 。

打开 `Docker Quickstart Terminal` 一开始就是 Docker 自动配置，其实就是它去下载一个叫做boot2docker.iso文件，就是 `default` 的镜像，然后在自己下载其他镜像的时候，不知道为什么连接 docker 的官方源的时候总会出问题，就无法下载新的镜像，这样肯定不行吖，就先搁置一边，继续折腾树莓派。

这个 default 的镜像同时也在你的 `Oracle VM VirtualBox` 里自动运行，直接进去不用密码，但是 ssh 上去需要用户名和密码

```
user: docker
pass: tcuser
```

于是想升级树莓派内核，看了一下网上的教程，还是挺复杂的。结果找到一个外国的把 Docker 移植到 树莓派上的系统 [hypriot](http://blog.hypriot.com/) ，在 [这篇文章](http://blog.hypriot.com/getting-started-with-docker-on-your-arm-device/) 中提到了将 Docker 安装到树莓派上，其实是它的系统自带 Docker ，最后就换了这个系统就好了。

这个 hypriot 的默认用户名和密码是 , 但是我登陆的时候用的用户名是 `root`

```
user: pirate
pass: hypriot
```

装好之后的效果。

![Raspberry_Docker](/images/Raspberry_Docker.png)

## 一些 Docker 指令

- `docker version` 查看 Docker 版本号
- `docker info` 查看 Docker 信息
- `docker images` 查看 Docker 镜像，在 Windows 上使用 Docker 会自带一个 `default` 的镜像，但是树莓派上不自带镜像
- `uname -a` 查看操作系统版本
- `docker ps` 查看所有在运行的 Docker 容器
- `docker ps -a` 查看所有的 Docker 容器
- `docker search ubuntu` 在 Docker 官方镜像源 `https://hub.docker.com/` 中寻找镜像
- `docker pull ubuntu` 在 Docker 官方镜像源中下载 Ubuntu 镜像，一般是 `作者名/镜像名` 的格式，但是像 Ubuntu 这种大众的不指定作者就用官方源
- `docker run -d -p 80:80 hypriot/rpi-busybox-httpd` 在本地镜像中寻找 hypriot/rpi-busybox-httpd 或者在远程官方镜像中寻找并下载，然后运行，同时将容器的 80 端口映射到本地的 80 端口
- `cat ubuntu-14.04-x86_64-minimal.tar.gz  |docker import - ubuntu:14.04` 官方推荐是从网上 pull 下来镜像，但是有时候太慢了，也可以自己先下载下来，然后再这样 import 进去

- `docker rm 8c342c0c275c` 删除 容器ID 为 8c342c0c275c 的容器
- `docker start 256d7bdde650` 开启已经停止的容器
- `docker stop 256d7bdde650` 关闭容器
- `docker attach 256d7bdde650` 连接到一个已经存在的容器，只有当另一个打开的时候
- `docker exec -t -i 256d7bdde650  /bin/bash` 连接到一个已经存在的容器，比 attach 好用
- `docker rm 'docker ps -a -q'` 删除所有的容器
- `docker rm 256d7bdde650` 删除容器
- `docker rmi sdhibit/rpi-raspbian` 删除镜像
- `docker logs 256d7bdde650` 查看容器的日志
- `docker inspect 256d7bdde650` 查看日志的实例属性
- `docker top 256d7bdde650` 显示容器的进程信息
- `docker port 256d7bdde650` 查看容器的端口映射情况
- `docker diff 256d7bdde650` 显示容器文件系统的前后变化
- `docker pause 256d7bdde650` 停止一个容器
- `docker unpause 256d7bdde650` 启动一个容器
- `docker commit –m 'add game 2048' 4807f56bb576 2048game` 将容器打包为镜像
- `docker exec <containerid> ip addr ` 查看容器IP地址，默认采用网桥连接方式

- `docker login` 登陆 Docker 官方镜像源，需要先在 `https://hub.docker.com/` 注册
- `docker push learn/ping` 发布自己的镜像
- `docker export XXX.tar` 将容器整个文件系统导出为一个tar包，不带layers、tag等信息
- `docker build .` 在当前目录下通过 Dockerfile 定制镜像
- `docker cp <containerId>:/file/path/within/container /host/path/target` 将容器中的文件拷贝到本地
- `docker create <imageid>` 创建一个新的容器，同 run，但不启动容器
- `docker exec <containerid> ls -al` 在已存在的容器上运行命令
- `docker kill 256d7bdde650` 杀死指定 docker 容器
- `docker load` 从一个 tar 包中加载一个镜像[对应 save]
- `docker restart` 重启运行的容器
- `docker save` 保存一个镜像为一个 tar 包[对应 load]
- `docker tag` 给源中镜像打标签
- `docker inspect jekyll` 查看某个容器或者镜像的信息

- `docker run -e MYSQL_ROOT_PASSWORD=123 -p 3306:3306 -t -i mysql` 创建并进入一个 MySQL 的容器

在进入容器之后，`exit` 可以退出容器，或者是 `Ctrl + P` 和 `Ctrl + Q`

## Docker 运行

```
HypriotOS: root@black-pearl in ~
$ docker version
Client version: 1.6.0
Client API version: 1.18
Go version (client): go1.4.2
Git commit (client): 4749651
OS/Arch (client): linux/arm
Server version: 1.6.0
Server API version: 1.18
Go version (server): go1.4.2
Git commit (server): 4749651
OS/Arch (server): linux/arm
HypriotOS: root@black-pearl in ~
$ docker info
Containers: 3
Images: 6
Storage Driver: overlay
 Backing Filesystem: extfs
Execution Driver: native-0.2
Kernel Version: 3.18.11-hypriotos+
Operating System: Raspbian GNU/Linux 7 (wheezy)
CPUs: 1
Total Memory: 434.2 MiB
Name: black-pearl
ID: 4UW5:N2GV:LGTL:UDM5:MCRB:O3CO:RVVH:YEXS:D4I5:EPWT:A6Z6:Y2JZ
Debug mode (server): true
Debug mode (client): false
Fds: 15
Goroutines: 80
System Time: Thu Sep 15 10:14:07 CEST 2016
EventsListeners: 0
Init SHA1: 9183200cc532e132ff6eac70172636ccc5a33724
Init Path: /usr/lib/docker/dockerinit
Docker Root Dir: /var/lib/docker
HypriotOS: root@black-pearl in ~
$ docker images
REPOSITORY                  TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
hypriot/rpi-busybox-httpd   latest              d0cb6fa4fa79        15 months ago       2.156 MB
sdhibit/rpi-raspbian        latest              e3ce6097d741        16 months ago       121.5 MB
HypriotOS: root@black-pearl in ~
$ uname -a
Linux black-pearl 3.18.11-hypriotos+ #1 PREEMPT Sun Apr 12 16:26:34 UTC 2015 armv6l GNU/Linux
HypriotOS: root@black-pearl in ~
$ docker ps -a
CONTAINER ID        IMAGE                              COMMAND                CREATED             STATUS                       PORTS                NAMES
f9ccede2524d        sdhibit/rpi-raspbian:latest        "/bin/bash"            14 minutes ago      Exited (127) 5 minutes ago                        prickly_turing
256d7bdde650        sdhibit/rpi-raspbian:latest        "/bin/bash"            About an hour ago   Exited (0) 15 minutes ago                         sad_galileo
60ca9b6c5c97        hypriot/rpi-busybox-httpd:latest   "/bin/busybox httpd    3 hours ago         Up 3 hours                   0.0.0.0:80->80/tcp   angry_euclid
HypriotOS: root@black-pearl in ~
$ docker search ubuntu
NAME                              DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
ubuntu                            Ubuntu is a Debian-based Linux operating s...   4707      [OK]
ubuntu-upstart                    Upstart is an event-based replacement for ...   66        [OK]
rastasheep/ubuntu-sshd            Dockerized SSH service, built on top of of...   41                   [OK]
ubuntu-debootstrap                debootstrap --variant=minbase --components...   27        [OK]
torusware/speedus-ubuntu          Always updated official Ubuntu docker imag...
```

## docker run 的参数

```
docker run [OPTIONS] IMAGE[:TAG] [COMMAND] [ARG...]
```

### OPTIONS

- `-p 80:80` 前一个为本地端口号，后一个为容器内端口号
- `-P` 自动映射端口，映射的端口将会从没有使用的端口池中 (49000..49900) 自动选择
- `-t` 分配一个（伪）tty (link is external)
- `-i` 交互模式 (so we can interact with it)
- `-d` 后台运行
- `--name` 给容器设定别名
- `--link <imagesid>:<imagename>` 连接另一个容器并设置别名
- `-e` 设定环境变量
- `-w` 设定工作目录
- `-v` 设定磁盘挂载，需为绝对路径
