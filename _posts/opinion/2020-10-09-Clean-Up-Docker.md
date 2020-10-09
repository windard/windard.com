---
layout: post
title: docker 清理技巧
description: docker 是真的好用，配置简单，随开随用，唯一的问题就是，不小心开的太多了，占用磁盘空间较大。
category: opinion
---

## 删除容器和镜像

最基本的操作，及时删除没用的容器或者镜像

```
# 查看所有容器
docker ps -a

# 删除容器
docker rm <container_id>

# 查看所有镜像
docker images -a
docker image ls

# 删除镜像
docker rmi <image_id>
```

## 删除数据卷和网络

一般用到的比较少，但是数据卷绑定很常见。
> 话虽然这样讲，但是一来不知道是哪个容器绑定的数据卷，二来数据卷绑定之后，在主机磁盘上也是有数据的吖，只删除容器内绑定磁盘么？那主机上数据也会被删除么？

```
# 查看所有绑定的数据卷
docker volume ls

# 删除绑定的数据卷
docker volume rm <volume_name>
```

对于不知道数据卷对应的容器，可以这样查看

```
docker ps -a -f volume=<volume_name>
```

关于网络，其实占用真的很小吧

```
# 查看网络设备
docker network ls

# 删除网络
docker network rm <network_id>
```

## 清理数据

### 删除停止的容器

对于一些已经停止的容器，可以进行删除,删除时会警告你是否真的要删除已经停止的容器，需要再次进行删除确认。
> 停止不代表没用，谨慎使用

```
docker container prune
```

### 清理无用的镜像

开启容器较多之后，可能会有一些临时的，没用的镜像文件，需要进行清理

> 同样在删除时会警告并再次确认，是否需要删除状态为 dangling (悬挂) 的镜像，状态为 dangling 的镜像为未被打标签(`<None>`)和没有被任何容器引用的镜像。

```
docker image prune

# 或者手动这样也行
docker rmi $(docker images -qf "dangling=true")
```

### 清理无用的数据卷和网络

删除未使用的数据卷

```
docker volume prune
```

删除未使用的网络连接

```
docker network prune
```

## 系统级指令

### 查看 docker 信息

```
docker system info
```

### 查看 docker 磁盘占用

```
# 查看容器，镜像和数据卷和缓存占用
docker system df 

# 具体查看每个容器，镜像，数据卷和缓存占用
docker system df -v
```

> 在看到绑定的容器数量为0的镜像，那肯定就可以删除了。   
> 在看到绑定的容器数量为0的数据卷，那肯定就可以删除了。

### 清理系统数据

```
docker system prune
```

主要包括
- all stopped containers
- all networks not used by at least one container
- all dangling images
- all dangling build cache

但是这里没有数据卷，如果想要清理数据卷，需要使用

```
docker system prune --volumes
```
