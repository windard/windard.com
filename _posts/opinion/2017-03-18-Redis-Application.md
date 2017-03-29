---
layout: post
title: redis 的一些典型应用
description: 使用 redis 完成 登陆错误次数限制, 网站站访问量统计。
category: opinion
---

redis 功能强大，不仅仅是 NoSQL 数据库 , 还有很多很强大的功能，简单易用。

## 网站访问量统计

可以对全站访问量进行简单的统计

```
# coding=utf-8

from flask import Flask, request
from flask_redis import FlaskRedis

app = Flask(__name__)
app.config.update({
    "REDIS_URL": "redis://127.0.0.1:6379/0"
})

redis_store = FlaskRedis(app)


@app.before_request
def before_request():
    setattr(request, 'view_times', redis_store.get(request.url))


@app.after_request
def after_request(f):
    redis_store.incr(request.url)
    return f


@app.route('/')
def index():
    return "This is the man paga , and it's your %s times view" % getattr(request, 'view_times')


@app.route('/page')
def page():
    return "I have seen you %s times" % getattr(request, 'view_times')


@app.route('/login')
def login():
    return "This is the %s times meet you ~" % getattr(request, 'view_times')

if __name__ == '__main__':
    app.run(port=5067, host='0.0.0.0')

```

## 登陆错误次数限制

在十分钟之内登陆错误五次，即不允许登陆

```
# coding=utf-8

import os
from flask import Flask, request, session, escape
from flask_redis import FlaskRedis

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': os.urandom(40),
    "REDIS_URL": "redis://127.0.0.1:6379/0"
})

redis_store = FlaskRedis(app)

form = """
        <form method="POST" action>
            <input type='test' name='name' >
            <input type='password' name='password'>
            <input type='submit' name='submit' value='登陆'>
        </form>
        """


@app.route('/')
def index():
    return "This is the index paga"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return form
    else:
        if redis_store.exists(request.remote_addr) and not int(redis_store.get(request.remote_addr)) < 5:
            return 'Login Failed overtimes , please try again later'
        if request.form.get('name') == 'windard' and request.form.get('password') == 'password':
            session['login'] = True
            session['username'] = 'windard'
            return 'Hello %s, Welcome back' % session['username']
        else:
            if redis_store.exists(request.remote_addr):
                redis_store.incr(request.remote_addr)
            else:
                redis_store.incr(request.remote_addr)
                redis_store.expire(request.remote_addr, 10 * 60)
            return 'Login Failed <br>' + form


if __name__ == '__main__':
    app.run(port=5067, host='0.0.0.0')

```


