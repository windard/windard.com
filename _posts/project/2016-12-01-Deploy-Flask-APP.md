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

也是一个有名的 python 网络库，不仅仅是 web 服务器，支持几乎所有的 reactor ，`--reactor=(options: "win32", "gi", "kqueue", "poll", "iocp", "select", "epoll", "gtk2", "gtk3", "wx", "default", "cf", "glib2")`

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

uWSGI 也是部署 web 服务的一种选择，其实也就是使用常见的 Nginx ， lighttpd 等 web 服务器来部署 Flask 项目。

## fastCGI

## CGI

不过这些方法用的都不多，最常见的还是用 web 服务器装载 Flask 应用，如 Apache，Nginx 等。

