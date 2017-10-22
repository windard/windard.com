---
layout: post
title: flask 中的 LocalProxy
description:  关于 flask 的深入学习
category: blog
---

Flask 有两个地方很重要，SessionInterface 和 LocalProxy

LocalProxy 只是一个中介，通过 LocalProxy 来查找全局变量

> 关于 SessionInterface 可以看[flask 中的 cookie 和 session](/blog/2017/10/17/Flask-Session)

Flask 全局有两个栈
1. `_request_ctx_stack.top`
2. `_app_ctx_stack.top`


第一个是当前请求的栈，第二个是当前应用的栈

选取应用全局变量则从当前应用栈顶取取出，如默认自带的 current_app

```
def _find_app():
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError('working outside of application context')
    return top.app

current_app = LocalProxy(_find_app)

```

也可以自己设定全局变量，如为当前请求设定一个全局的 current_user

```
def set_current_user(user):
    setattr(_request_ctx_stack.top, 'user', user)

```

然后就可以从当前请求的栈顶取出 current_user 。

Flask 还提供了一个 `_lookup_req_object` 和 `_lookup_app_object` ，用来方便的从栈顶取全局变量

```
def _lookup_req_object(name):
    top = _request_ctx_stack.top
    if top is None:
        raise RuntimeError('working outside of request context')
    return getattr(top, name)

```

只不过使用比较麻烦，如全局变量 g

```
g = LocalProxy(partial(_lookup_app_object, 'g'))

```

> 关于 partial 的使用可以看我的[这篇博客](https://github.com/windard/Python_Lib/blob/master/content/functools.md)

最后，至于这两个栈是什么？LocalStack。
