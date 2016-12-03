---
layout: post
title: Flask 的部署
category: project
description: 主要是在腾讯云上部署 Flask 应用
---

## flask 自行运行

让 Flask 程序运行起来的方法有很多，Flask 程序自己就能够运行。

```
# coding=utf-8

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

然后直接 ` python hello.py ` 运行即可

```
C:\Users\dell\.ssh\Flasky\test (master)
λ python hello.py
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
```

或者用 flask_script 也可以，其实还是 flask 自己运行，只不过多加了一些参数。

```
# coding=utf-8

from flask import Flask
from flask_script import Manager, Shell

app = Flask(__name__)
manager = Manager(app)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    manager.run()
```

然后使用 `python hello.py runserver` 来运行。

```
C:\Users\dell\.ssh\Flasky\test (master)
λ python hello.py runserver --host 0.0.0.0 --port 8090
 * Running on http://0.0.0.0:8090/ (Press CTRL+C to quit)
```

flask 自己运行的时候，是单线程的，所以效率不是太高，不过可以通过添加一个 `threaded=True` 或 `--threaded` 的参数来实现多线程的 web 服务器。

## WSGI

WSGI (Web Server Gateway Interface) 服务器网关接口，它并不是一个库，而是一类提供 web 服务器功能的库。

### gunicorn

使用 pip 安装，然后同样的文件使用 `gunicorn hello:app` 来运行，不过 gunicorn 用到一个 fcntl 的库，用来做文件锁，只在 POSIX 下使用，在 Windows 下没有。它是使用 pre-fork 的 web 服务器，好像不是多进程，但是又不知道是什么。

```
[root@VM_22_223_centos test]# gunicorn hello:app -b 0.0.0.0:8888
[2016-12-01 20:44:37 +0000] [27231] [INFO] Starting gunicorn 19.6.0
[2016-12-01 20:44:37 +0000] [27231] [INFO] Listening at: http://0.0.0.0:8888 (27231)
[2016-12-01 20:44:37 +0000] [27231] [INFO] Using worker: sync
[2016-12-01 20:44:37 +0000] [27236] [INFO] Booting worker with pid: 27236
^C[2016-12-01 20:44:39 +0000] [27231] [INFO] Handling signal: int
[2016-12-01 20:44:39 +0000] [27236] [INFO] Worker exiting (pid: 27236)
[2016-12-01 20:44:39 +0000] [27231] [INFO] Shutting down: Master
```

参数 `-b(--bind)` 绑定主机和端口号，`-w(--workers)` 指定工作进程数，`-p(--pid)` 指定 pid ，`--threads` 指定线程数，`-D(--daemon)` 作为守护进程。

### Gevent

这是一个用 协程 实现的 web 服务器，效率也还是可以的。

```
# coding=utf-8

from flask import Flask
from gevent.wsgi import WSGIServer

app = Flask(__name__)
http_server = WSGIServer(('', 8080), app)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    http_server.serve_forever()
```

然后同样的方法启动即可。

### Twisted

也是一个有名的 python 基于事件驱动的网络框架，不仅仅是 web 服务器，支持几乎所有的 reactor ，`--reactor=(options: "win32", "gi", "kqueue", "poll", "iocp", "select", "epoll", "gtk2", "gtk3", "wx", "default", "cf", "glib2")`

这样启动

```
twistd web --wsgi myproject.app
```

或者这样也可以

```
twistd -n web --port 8080 --wsgi myproject.app
```

虽然上面的这些使用 WSGI 程序一般也能监听外网，但是为了防止 DDOS 攻击或其他危害，都是监听内网，所以我们还需要一个反向代理来监听对外端口，一般采用 Nginx 或者 Apache。

Nginx 配置文件

```
server {
    listen 80;

    server_name _;

    access_log  /var/log/nginx/access.log;
    error_log  /var/log/nginx/error.log;

    location / {
        proxy_pass         http://127.0.0.1:8000/;
        proxy_redirect     off;

        proxy_set_header   Host                 $host;
        proxy_set_header   X-Real-IP            $remote_addr;
        proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto    $scheme;
    }
}
```

## uWSGI

uWSGI 也是部署 web 服务的一种选择，它也是基于 WSGI 的，但是它将这些封装到了底层，提供更多的选择，常见的 web 服务器，如 Nginx，lighttpd 等都支持 uWSGI。

uWSGI 本身就能够驱动 Flask 程序运行，同样是最上面的那个 Flask 文件，监听 127.0.0.1:3031 ，使用 4 个进程，2 个线程，监控端口在 127.0.0.1:9091.

```
uwsgi --http 127.0.0.1:3031 --wsgi-file hello.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191
```

或者是写入一个 uWSGI 配置文件 `uwsgi.ini` 中。

```
[uwsgi]

http = 127.0.0.1:3001

chdir = /root/test

wsgi-file = test.py

callable = app

processes = 4

threads = 2

stats = 127.0.0.1:9091

``` 

然后使用 `uwsgi uwsgi.ini` 来运行。

虽然这样也是可以用的，但是直接用 uWSGI 来作为 web 服务器还是比较危险的，一般的作法是将 uWSGI 作为后端服务器，然后使用 Nginx 做反向代理，将前端请求转发到 uWSGI 服务器，这样就可以用 Nginx 做负载均衡，抗 DDOS 攻击等。

将 uWSGI 作为后端服务器 和 将 uWSGI 直接作为服务器的最主要区别就是直接服务器的话服务器类型就是 http ，而作为后端服务器则是作为 一个 socket ，在 Nginx 里处理请求内容。所以作为直接服务器就可以使用浏览器访问，而作为一个 socket 组件则不能直接接受请求。

使用 uWSGI 启动 Flask 作为后端服务器

```
uwsgi --socket 127.0.0.1:3031 --wsgi-file hello.py  --callable app --master --processes 4 --threads 2 --stats 127.0.0.1:9191
```

使用配置文件则是

```
[uwsgi]

socket = 127.0.0.1:8001     //启动程序时所使用的地址和端口，通常在本地运行flask项目，
                            //地址和端口是127.0.0.1:5000,
                            //不过在服务器上是通过uwsgi设置端口，通过uwsgi来启动项目，
                            //也就是说启动了uwsgi，也就启动了项目。
chdir = /home/www/     //项目目录

wsgi-file = manage.py      //flask程序的启动文件，通常在本地是通过运行  
                           //      python manage.py runserver 来启动项目的

callable = app      //程序内启用的application变量名

processes = 4     //处理器个数

threads = 2     //线程个数

stats = 127.0.0.1:9191      //获取uwsgi统计信息的服务地址
```

然后在 Nginx 配置

```
location / {
    include uwsgi_params;
    uwsgi_pass 127.0.0.1:3031;
}
```

除了配置本地端口通过 socket 之外，还能直接通过 sock 来传递请求。

```
uwsgi -s /tmp/uwsgi.sock --chmod-sock=666 -H /home/victor/demo --module helloworld -callable app
```

配置文件是

```
[uwsgi]
socket = /run/uwsgi/flask/socket
chdir = /root/test
master = true
file = test.py
pidfile = /opt/flask/uwsgi.pid
uid = www-data
gid = www-data
log-date = true
logto = /var/log/uwsgi/uwsgi-emperor.log
```

## fastCGI

## CGI

不过这些方法用的都不多，最常见的还是用 web 服务器装载 Flask 应用，如 Apache，Nginx 等。

