---
layout: post
title: Flask 的部署
category: project
description: 主要是用各种方式在服务器上部署 Flask 应用
---

## flask 自己运行

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

flask 自己运行的时候，是单线程的，所以效率不是太高，不过可以通过添加一个 `threaded=True` 或 `--threaded` 的参数来实现多线程的 web 服务器，用 `processes=True` 或 `--processes` 的参数来实现多进程的 web 服务器。

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

也是一个有名的 python 基于事件驱动的网络框架，不仅仅是 web 服务器。

这样启动

```
twistd web --wsgi myproject.app
```

或者这样也可以

```
twistd -n web --port 8080 --wsgi myproject.app
```

> 关于 Twist ，这是 Flask 官方提供的运行方式，然而我并没有将其运行起来。。。

虽然上面的这些使用 WSGI 程序能监听外网，但是为了防止 DDOS 攻击或其他危害，一般都是监听内网，然后使用一个反向代理来监听对外端口，一般采用 Nginx 或者 Apache。

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

socket = 127.0.0.1:3031     // 启动程序时所使用的地址和端口，通常在本地运行flask项目，
                            // 地址和端口是127.0.0.1:5000,
                            // 不过在服务器上是通过uwsgi设置端口，通过uwsgi来启动项目，
                            // 也就是说启动了uwsgi，也就启动了项目。
chdir = /home/www/          // 项目目录

wsgi-file = manage.py       // flask程序的启动文件，通常在本地是通过运行  
                            // python manage.py runserver 来启动项目的

callable = app              // 程序内启用的application变量名

processes = 4               // 处理器个数

threads = 2                 // 线程个数

stats = 127.0.0.1:9191      // 获取uwsgi统计信息的服务地址
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
uwsgi -s /var/www/uwsgi.sock --chmod-sock=666 --wsgi-file hello.py --callable app
```

或者使用配置文件

```
[uwsgi]
socket = /var/www/uwsgi.sock

chmod-socket = 666

chdir = /root/python

wsgi-file = hello.py

master = true

callable = app

processes = 4

threads = 2

log-date = true

logto = /var/log/uwsgi.log

stats = 127.0.0.1:9091
```

Nginx 的配置文件也是一样的

```
location / {
    include uwsgi_params;
    uwsgi_pass unix:/var/www/uwsgi.sock;

    proxy_set_header   Host                 $host;
    proxy_set_header   X-Real-IP            $remote_addr;
    proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;
    proxy_set_header   X-Forwarded-Proto    $scheme;
}
```

## 其他

`fastCGI`,`CGI` 不过这些方法用的都不多，最常见的还是上面写到的那些。

那么接下来我们就来试一下上面的那些的性能吧。

测试命令 `siege -c 1000 -r 100 -b http://127.0.0.1:8090` 

### 纯原生

```
Transactions:                  25416 hits
Availability:                  99.67 %
Elapsed time:                  42.07 secs
Data transferred:               0.29 MB
Response time:                  0.29 secs
Transaction rate:             604.14 trans/sec
Throughput:                     0.01 MB/sec
Concurrency:                  177.53
Successful transactions:       25416
Failed transactions:              84
Longest transaction:           31.62
Shortest transaction:           0.00
```

### 纯原生 + 多线程

```
Transactions:                  25428 hits
Availability:                  99.72 %
Elapsed time:                  38.42 secs
Data transferred:               0.29 MB
Response time:                  0.25 secs
Transaction rate:             661.84 trans/sec
Throughput:                     0.01 MB/sec
Concurrency:                  162.77
Successful transactions:       25428
Failed transactions:              72
Longest transaction:           31.14
Shortest transaction:           0.03
```

### 纯原生 + 多进程

```
Transactions:                  25394 hits
Availability:                  99.58 %
Elapsed time:                  39.28 secs
Data transferred:               0.29 MB
Response time:                  0.25 secs
Transaction rate:             646.49 trans/sec
Throughput:                     0.01 MB/sec
Concurrency:                  163.27
Successful transactions:       25394
Failed transactions:             106
Longest transaction:           31.21
Shortest transaction:           0.00
```

### gunicorn

```
Transactions:                  25500 hits
Availability:                 100.00 %
Elapsed time:                  38.94 secs
Data transferred:               0.29 MB
Response time:                  0.38 secs
Transaction rate:             654.85 trans/sec
Throughput:                     0.01 MB/sec
Concurrency:                  249.79
Successful transactions:       25500
Failed transactions:               0
Longest transaction:            1.61
Shortest transaction:           0.01
```

### Gevent

```
Transactions:                  25500 hits
Availability:                 100.00 %
Elapsed time:                  25.33 secs
Data transferred:               0.29 MB
Response time:                  0.22 secs
Transaction rate:            1006.71 trans/sec
Throughput:                     0.01 MB/sec
Concurrency:                  221.98
Successful transactions:       25500
Failed transactions:               0
Longest transaction:           15.15
Shortest transaction:           0.00
```

### uwsgi

```
Transactions:                  25500 hits
Availability:                 100.00 %
Elapsed time:                  49.84 secs
Data transferred:               0.29 MB
Response time:                  0.30 secs
Transaction rate:             511.64 trans/sec
Throughput:                     0.01 MB/sec
Concurrency:                  154.09
Successful transactions:       25500
Failed transactions:               0
Longest transaction:           46.09
Shortest transaction:           0.00
```

### uwsgi + Nginx

```
Transactions:                  25475 hits
Availability:                  99.90 %
Elapsed time:                  19.71 secs
Data transferred:               0.29 MB
Response time:                  0.14 secs
Transaction rate:            1292.49 trans/sec
Throughput:                     0.01 MB/sec
Concurrency:                  175.43
Successful transactions:       25475
Failed transactions:              25
Longest transaction:           15.11
Shortest transaction:           0.00
```

### Tornado

类似的代码

```
# coding=utf-8

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello World!")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8090)
    tornado.ioloop.IOLoop.current().start()
```

```
Transactions:                  25429 hits
Availability:                  99.72 %
Elapsed time:                  35.99 secs
Data transferred:               0.29 MB
Response time:                  0.21 secs
Transaction rate:             706.56 trans/sec
Throughput:                     0.01 MB/sec
Concurrency:                  151.04
Successful transactions:       25429
Failed transactions:              71
Longest transaction:           31.05
Shortest transaction:           0.00
```

虽然设定的是每次 1000 个，但是好像是限制并发数255。

感觉是不是页面太简单了，好像并没有多大的差距。。。

不过还是可以看到 uwsgi + Nginx 是最强组合。

使用 Nginx + PHP 

```
Transactions:                  25478 hits
Availability:                  99.91 %
Elapsed time:                  16.54 secs
Data transferred:               0.29 MB
Response time:                  0.09 secs
Transaction rate:            1540.39 trans/sec
Throughput:                     0.02 MB/sec
Concurrency:                  141.94
Successful transactions:       25478
Failed transactions:              22
Longest transaction:           15.02
Shortest transaction:           0.00
```
