---
layout: post
title: Linux 下服务创建服务管理应用程序
description:  使用 Linux Service 运行管理服务, 功能强大，使用方便。
category: blog
---

## Linux Service

Linux 下的 Service 可以用来管理一个服务的启动，重启，关闭等整个生命周期，使用更方便，和 make 构建工具相比，make 更像是管杀不管埋。

在 CentOS 下，以前都是用 `service xxxx start` 来启动服务的，现在也可以使用 `systemctl start xxxx` 执行动作和服务名的位置互换了。

但是其实 `service` 和 `systemctl` 的底层已经换软件了，之前是用 `initd` 来管理控制 Linux 系统守护进程，现在用的是 `systemd`

![systemd](/images/systemd.png)

写好的 Service 服务文件，一般位于 `/etc/systemd/system` 下,系统级别的服务在 `/lib/systemd/system` 下，这个地址其实是 `/usr/lib/systemd/system` 的一个软链。

整个服务脚本，分为三个部分 Unit,Service,Install 

举个例子, 非常简单的运行 python flask 代码。

```
[Unit]
Description=Flask App
After=network.target

[Service]
WorkingDirectory=/opt/heroku-python
ExecStart=/root/miniconda3/bin/python flasky.py

[Install]
WantedBy=multi-user.target
```

### Unit

控制单元，每个单元中的的介绍信息和启动顺序和依赖顺序。

介绍信息

- Description: 描述信息
- Documentation: 文档信息或者文档位置

启动顺序

- Before: 在什么服务之前启动
- After: 在什么服务之后启动，如果前一个服务未启动，后一个服务无法运行

依赖顺序，与启动顺序无关，默认可以同时启动

- Wants: 弱依赖，如果依赖服务挂了，那还可以继续运行
- Requires: 强依赖，如果依赖服务挂了，那自己也要结束

### Service

服务定义

#### 启动命令

每个单元中的启动命令。根据程序运行顺序，有六个执行时机。

- PIDFile: 服务的进程号 PID 文件路径
- EnvironmentFile: 环境变量的文件，文件中以键值对的形式存储，可以用 $key 的方式在配置文件中获取
- ExecStartPre: 启动前命令
- ExecStart: 主程序启动命令
- ExecStartPost: 启动后命令
- ExecReload: 服务重载命令
- ExecStop: 主程序停止命令
- ExecStopPost: 主程序停止后命令

其中有几点需要注意
1. 启动前和启动后命令都可以设置多条，依次顺序执行，但是启动，关闭和重载命令只能设置一条，使用空字符串清空之前设置，如果强行多次设置会报错。
2. 在命令中使用绝对路径，不要使用相对路径。
3. 在停止和重载命令中可以使用 `$MAINPID` 代表主程序进程号
4. 同时缺少 ExecStart 与 ExecStop 的服务单元是非法的，也就是必须至少明确设置其中之一
5. 如果在绝对路径前加上可选的 "-" 前缀，那么即使该进程以失败状态(例如非零的返回值或者出现异常)退出，也会被视为成功退出，但同时会留下错误日志。

举个例子

```
[Unit]
Description=Signal App
After=network.target

[Service]
WorkingDirectory=/opt/heroku-python
ExecStartPre=/usr/bin/echo before start
ExecStart=/root/miniconda3/bin/python kill_signal.py
ExecStartPost=/usr/bin/echo after start
ExecReload=/bin/kill -HUP $MAINPID
ExecStop=/bin/kill -INT $MAINPID
ExecStopPost=/usr/bin/echo after stop

[Install]
WantedBy=multi-user.target
```

```
# -*- coding: utf-8 -*-

import os
import time
import logging
import signal

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(name)-25s %(asctime)s %(levelname)-8s %(lineno)-4d %(message)s',
    datefmt='[%Y %b %d %a %H:%M:%S]',
)


def receive_signal(signum, stack):
    logger.info('Received: %s', signum)


if __name__ == '__main__':

    # Register signal handlers
    signal.signal(signal.SIGHUP, receive_signal)
    signal.signal(signal.SIGINT, receive_signal)
    signal.signal(signal.SIGQUIT, receive_signal)
    # signal.signal(signal.SIGKILL, receive_signal)
    signal.signal(signal.SIGTERM, receive_signal)
    signal.signal(signal.SIGTSTP, receive_signal)
    signal.signal(signal.SIGCONT, receive_signal)

    signal.signal(signal.SIGUSR1, receive_signal)
    signal.signal(signal.SIGUSR2, receive_signal)

    # Print the process ID so it can be used with 'kill'
    # to send this program signals.
    logger.info('My PID is: %s', os.getpid())

    for i in range(20):
        logger.info('Waiting...')
        time.sleep(30)

```

程序运行十分钟，可以用接收信号并打印出来。

运行过程多次调试后发现，其实一般程序代码只需要配置 ExecStart 即可。

如果有 reload 需求，则配置一下 `ExecReload=/bin/kill -HUP $MAINPID`

然后 stop 是可以不用配置的，因为提供 ExecStop 只是给一个体面的结束方式，如果能体面的结束，systemd 就让程序体面的结束，如果不能体面的结束，systemd 就让程序体面的结束。

在单元停止时，默认会对单元里的 services 所有进程都发送一个 SIGTERM 的结束信号，然后立刻紧接着再发送一个 SIGCONT 信号，杀死并挂起大礼包之后，已经相当于 kill 了所有进程，死的体面。

在等待结束超时时间之后，默认是 90 秒，如果进程还没死，就会再发送一个 SIGKILL ，强行杀死进程，死的干净。 

不过这些都是可以配置的，具体详见 [systemd.kill 中文手册](http://www.jinbuguo.com/systemd/systemd.kill.html#)

#### 启动类型

Type 定义单元的启动类型，默认为 simple 
- simple: 简单类型，运行 ExecStart 的命令，service 是用来创建管理守护进程的，所以这里最好不是一个守护进程，也就是最好是一个启动之后持续运行的程序，而不是启动之后即消失或者结束，这样服务的运行状态也会变成 inactive 
- forking: 也是比较常见的启动类型，用 forking 创建子进程的方式执行 ExecStart 中的命令，执行结束后父进程退出，子进程作为主进程。
- oneshot: 类似于 simple ，但是只执行一次 ，systemd 会等他执行完，再启动其他服务。但是前面的一点说的比较牵强，不知道是什么意思，不如说它可以设置多个 ExecStart 启动命令，依次执行比较实在。
- dbus: 用的较少，等待 D-Bus 信号后启动
- notify: 用的较少，启动结束后会发出 notify 的信号
- idle: 用的较少，等其他进程启动后再执行。

如果启动运行命令确实不是一个可以持续运行的程序，也可以通过设置 `RemainAfterExit=yes` 让服务启动后，就认为其还在活跃状态。

举个例子

```
(base) [root@vultrguest system]# systemctl cat once
# /etc/systemd/system/once.service
[Unit]
Description=Once App
After=flasky.service

[Service]
#Type=oneshot
ExecStartPre=/usr/bin/echo before once start
#ExecStart=/usr/bin/echo start
ExecStart=/usr/bin/echo start again
ExecStartPost=/usr/bin/echo after one start
ExecReload=/usr/bin/echo once reload
ExecStop=/usr/bin/echo stop once stop
ExecStopPost=/usr/bin/echo after once stop
RemainAfterExit=yes
(base) [root@vultrguest system]# systemctl start once
(base) [root@vultrguest system]# systemctl status once
● once.service - Once App
   Loaded: loaded (/etc/systemd/system/once.service; static; vendor preset: disabled)
   Active: active (exited) since Fri 2020-06-26 18:14:25 UTC; 26s ago
  Process: 10472 ExecStartPost=/usr/bin/echo after one start (code=exited, status=0/SUCCESS)
  Process: 10471 ExecStart=/usr/bin/echo start again (code=exited, status=0/SUCCESS)
  Process: 10470 ExecStartPre=/usr/bin/echo before once start (code=exited, status=0/SUCCESS)
 Main PID: 10471 (code=exited, status=0/SUCCESS)

Jun 26 18:14:25 vultrguest systemd[1]: Starting Once App...
Jun 26 18:14:25 vultrguest echo[10470]: before once start
Jun 26 18:14:25 vultrguest echo[10471]: start again
Jun 26 18:14:25 vultrguest echo[10472]: after one start
Jun 26 18:14:25 vultrguest systemd[1]: Started Once App.
```

status 的输出
- Loaded: 配置文件的位置，是否启用开机启动
- Active: 是否在活跃状态，启动时间
- Process: 执行命令配置
- Main PID: 主程序进程号
- 日志: 最多展示十条日志

#### 自动重启

在服务启动时，或许会因为某些原因而启动失败，是否配置重启。
- Restart: 默认为 no，表示不重启，可选值有:on-success,on-failure,on-abnormal,on-abort,on-watchdog,always
- RestartSec: 在重启服务之前，暂停多久，默认 100ms，但是配置时间默认单位为秒。
- TimeoutStartSec: 启动超时时间，如果超过指定时间，还未发出 启动完成的信号，则认为启动超时，默认启动超时时间 90秒
- TimeoutStopSec: 关闭超时时间，如果超过少时时间，还未结束程序，则认为关闭失败，会强行发出 SIGKILL 的信号，关闭程序，默认是 90秒。
- TimeoutSec: 同时设置 TimeoutStartSec 和 TimeoutStopSec
- RuntimeMaxSec: 程序运行运行的最大时间，默认是 `infinity` 不限。如果超过时间，程序会被强制终止，并被认为是失败状态。

#### 用户组

- User: 程序运行的 user
- Group: 程序运行的 user group，所属的用户组

### Install

安装部分，如何配置开机启动

主要命令 `WantedBy` 该服务所在的服务组，可以通过 `systemctl get-default` 获取默认的服务组，一般都是 `multi-user.target`.

实际上，一般常用的就两个服务器
- multi-user.target: 表示多用户命令行状态
- graphical.target: 图形化界面状态，不过也是依赖于 `multi-user.target`

所以在使用 `systemctl enable xxxx` 配置开机启动之后，配置文件会被创建软链到 `/etc/systemd/system/multi-user.target.wants` 中。


## 使用命令

查看所有服务单元

```
systemctl list-units 		
```

列出所有配置文件

```
systemctl list-unit-files
```

重新加载修改过的服务配置文件

```
systemctl daemon-reload
```

只要写一个 `ExecStart` ，就会自动配置启动，关闭和重启命令

```
systemctl start gunicorn  			# 启动
systemctl stop gunicorn  			# 关闭
systemctl restart gunicorn  		# 重启
```

然后可以查看运行状态

```
systemctl status 					# 查看系统状态
systemctl status gunicorn 			# 查看运行状态
systemctl show gunicorn 			# 查看服务详情
systemctl cat gunicorn 				# 查看配置文件
```

还有开机启动和关闭开机启动

```
systemctl enable gunicorn  				# 开启启动
systemctl disable gunicorn  			# 关闭开机启动
```

如果你需要开机启动的话，使用 `systemctl enable xxxx` 来开启，然后就会在 `/etc/systemd/system/multi-user.target.wants`  中建一个软链，如果你的 Target 是 multi-user 的话。

## Systemd

Systemd 是 Linux 系统工具，不仅仅是用来管理服务，而且是管理整个 Linux 的系统启动周期。

systemctl是 Systemd 的主命令，用于管理系统。

```
# 重启系统
$ sudo systemctl reboot

# 关闭系统，切断电源
$ sudo systemctl poweroff

# CPU停止工作
$ sudo systemctl halt

# 暂停系统
$ sudo systemctl suspend

# 让系统进入冬眠状态
$ sudo systemctl hibernate

# 让系统进入交互式休眠状态
$ sudo systemctl hybrid-sleep

# 启动进入救援状态（单用户状态）
$ sudo systemctl rescue
```

systemd-analyze 命令用于查看启动耗时。

```

# 查看启动耗时
$ systemd-analyze                                                                                       

# 查看每个服务的启动耗时
$ systemd-analyze blame

# 显示瀑布状的启动过程流
$ systemd-analyze critical-chain

# 显示指定服务的启动流
$ systemd-analyze critical-chain atd.service
```

hostnamectl 命令用于查看当前主机的信息。

```
# 显示当前主机的信息
$ hostnamectl

# 设置主机名。
$ sudo hostnamectl set-hostname rhel7
```

localectl 命令用于查看本地化设置。

```
# 查看本地化设置
$ localectl

# 设置本地化参数。
$ sudo localectl set-locale LANG=en_GB.utf8
$ sudo localectl set-keymap en_GB
```

timedatectl 命令用于查看当前时区设置。

```
# 查看当前时区设置
$ timedatectl

# 显示所有可用的时区
$ timedatectl list-timezones                                                                                   

# 设置当前时区
$ sudo timedatectl set-timezone America/New_York
$ sudo timedatectl set-time YYYY-MM-DD
$ sudo timedatectl set-time HH:MM:SS
```

loginctl 命令用于查看当前登录的用户。

```
# 列出当前session
$ loginctl list-sessions

# 列出当前登录用户
$ loginctl list-users

# 列出显示指定用户的信息
$ loginctl show-user root
```

## 日志管理

使用 `status` 只能看到最后的10条日志，如果想要看到完整的日志使用 `journalctl -u flasky` , 加上 `-f` 实时滚动。

实际上 `journalctl` 是用来查看全部的 Linux 系统启动服务日志的,配置文件在 `/etc/systemd/journald.conf`

之前使用 `dmesg` 查看系统启动日志 使用 `journalctl` 也可以用来查看启动日志，`journalctl -k` 只看内核日志。		

功能强大，用法很多，抄一份过来

```
# 查看所有日志（默认情况下 ，只保存本次启动的日志）
$ sudo journalctl

# 查看内核日志（不显示应用日志）
$ sudo journalctl -k

# 查看系统本次启动的日志
$ sudo journalctl -b
$ sudo journalctl -b -0

# 查看上一次启动的日志（需更改设置）
$ sudo journalctl -b -1

# 查看指定时间的日志
$ sudo journalctl --since="2012-10-30 18:17:16"
$ sudo journalctl --since "20 min ago"
$ sudo journalctl --since yesterday
$ sudo journalctl --since "2015-01-10" --until "2015-01-11 03:00"
$ sudo journalctl --since 09:00 --until "1 hour ago"

# 显示尾部的最新10行日志
$ sudo journalctl -n

# 显示尾部指定行数的日志
$ sudo journalctl -n 20

# 实时滚动显示最新日志
$ sudo journalctl -f

# 查看指定服务的日志
$ sudo journalctl /usr/lib/systemd/systemd

# 查看指定进程的日志
$ sudo journalctl _PID=1

# 查看某个路径的脚本的日志
$ sudo journalctl /usr/bin/bash

# 查看指定用户的日志
$ sudo journalctl _UID=33 --since today

# 查看某个 Unit 的日志
$ sudo journalctl -u nginx.service
$ sudo journalctl -u nginx.service --since today

# 实时滚动显示某个 Unit 的最新日志
$ sudo journalctl -u nginx.service -f

# 合并显示多个 Unit 的日志
$ journalctl -u nginx.service -u php-fpm.service --since today

# 查看指定优先级（及其以上级别）的日志，共有8级
# 0: emerg
# 1: alert
# 2: crit
# 3: err
# 4: warning
# 5: notice
# 6: info
# 7: debug
$ sudo journalctl -p err -b

# 日志默认分页输出，--no-pager 改为正常的标准输出
$ sudo journalctl --no-pager

# 以 JSON 格式（单行）输出
$ sudo journalctl -b -u nginx.service -o json

# 以 JSON 格式（多行）输出，可读性更好
$ sudo journalctl -b -u nginx.serviceqq
 -o json-pretty

# 显示日志占据的硬盘空间
$ sudo journalctl --disk-usage

# 指定日志文件占据的最大空间
$ sudo journalctl --vacuum-size=1G

# 指定日志文件保存多久
$ sudo journalctl --vacuum-time=1years
```

## 参考文档

[Systemd 入门教程：命令篇](http://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-commands.html) <br>
[Systemd 入门教程：实战篇](https://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-part-two.html) <br>
[systemd.service 中文手册](http://www.jinbuguo.com/systemd/systemd.service.html) <br>
[How To Set Up Django with Postgres, Nginx, and Gunicorn on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04) <br>
