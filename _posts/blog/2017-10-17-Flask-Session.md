---
layout: post
title: flask 中的 cookie 和 session
description:  Flask 可以满足你对 web 的所有想象
category: blog
---

session 和 cookie ，web 开发中必知必会必须掌握的两个概念。
- cookie 小饼干，存储在用户浏览器，在用户发起HTTP请求时，一起发给 web 后端，标志用户身份
- session 会话，在 web 后端记录用户的登录状态，保存方式有 cookie，内存，缓存，数据库等，用来区分不同用户的请求，和同一个用户的不同请求

## flask 的原生 session 实现

session 能够区分不用的用户请求和同一个用户的不同请求，则需要将每一个请求的 session 数据隔离，即保证每一个请求的 session 数据不能相互混淆，每一个 session 的数据都只属于本次请求，其他请求不能拿到。在 flask 中，作为一次请求的的全局变量，session 数据是从本次请求的栈顶取出，详细可以查看 [flask 的 LocalProxy](/blog/2017/10/12/Flask-LocalProxy)

在每一个请求的时候，session 数据是栈顶取出，那么不在这次请求的时候，session 存储在哪里呢？

Flask 中默认是直接将 服务器端的 session 存储在客户端浏览器的 cookie 中，当然是加密过的，意思就是说，后端在 session 里面写入什么数据，就会被加密存储到客户端 cookie 里面，浏览器中那条叫做 session 的 cookie 就是加密数据，只要你明白算法，知道密钥，理论上就可以把 session 的数据都算出来，所以在 flask 中如果想要使用 session 就必须要设一个 SECRET_KEY ，这就是 session 加密的密钥。

将 session 放在 cookie 中有好处，也有坏处。好处是不受服务器端影响，flask 重启仍然可以使用，如果放在内存中，后端重启，前端全部需要再次登录。坏处是如果存很多数据在 session 里面，那么 cookie 就会非常大，而前端是不应该存储大量数据，而且容易被人破解，虽然即使是同样的 session 数据，每次加密生成 cookie 也不同，但是也还是不安全，怪不得 cookie 中的这条数据叫做 session，而不是session_id 或者 sid。

Session 可以看做是一个类字典对象，存储序列化的数据，它不能直接存储对象，需要将对象序列化之后存储，数组字典都可以，但是对象不行。

既然 session 是一个字典，那它是怎样保持登录状态的呢？那它是怎样知道两次请求时同一个用户的呢？

只要 session 在每一个请求中是隔离的，那只需要在 session 中存储 `login=True` 的键值对，那么只要 session 中有这样的键值对，即可以表明发起该次请求的用户是登录的。每一次请求的 session 是隔离的，那么在 session 中存储 `user_id=xxx`，如果某两次请求的 `user_id` 是相同的，那么这两次请求的用户即是相同的。

## flask 使用 sid

阅读 flask 源代码 `sessions.py` 中的 `SecureCookieSessionInterface`,这是 flask 默认的 SessionInterface.

根据源代码可以发现 session 的导入和导出主要由 `open_session` 和 `save_session` 负责，前者从请求的 cookie 中取出 session ，然后解密反序列化，返回一个 `session_class`,如果没有找到 session ，则返回一个空的 `session_class`,后者负责将 session 序列化加密，放入返回响应头中。

那手动实现 session_id 的功能也非常的简单，在存入 cookie 的时候，不直接存储存储加密之后的 session ，而是使用 sha1 计算出 session 的哈希值，作为索引，然后将其存入 Redis 缓存中，然后将哈希值提供给前端。在取出 cookie 的时候，通过哈希值来查找到 session 的内容，这样在传给前端页面的 cookie 也能够保证一个好看的，长度固定的 sid ，无法猜测，无法破解。

将 session 放在 cookie 中，还有一个很大的安全隐患，虽然即使是相同的 session 数据，每一次加密之后的结果也会不同，因为引入了时间戳作为校验，但是这也就说明只要在 cookie 有效期之内，那每一次请求的 cookie 都可以继续使用，都可以自动登录，获得登录状态。

使用 sid的时候，每次的请求 sid 也会有所改变，为了安全，可以在每次从 Redis 缓存中取出 session 数据的时候，也同时删除缓存数据，就可以避免使用以前的 sid 登录，同时也是为了避免缓存中存储大量的无用数据，如果每次登录都是一条新的缓存数据，用户量大的情况下，Redis 也受不了吖。

而且使用 Redis 缓存将 sid 与 session 加密结果一起存储的方式，与 flask 无关，在后端重启之后照样可以正常拿到数据，存到 Redis 里面也可以比较稳。

所以总结就是即使是在 cookie 里面存储 session 的加密值，每一次刷新页面也会刷新 cookie，将 cookie 换上新的时间戳之类的，加密的结果是不一致的，虽然大部分数据段的内容是相同的。在使用sid的时候则会特别的明显，每次都是不一样的结果。

使用 sid 的话，如果之前的sid还在有效期之内的话，理论上说拿着之前的sid，也是可以使用的，所以需要将sid从缓存中每次取出后删除，使用sid，只取用一次，就从Redis中删除，避免Redis占用过大。

默认的 cookie 的有效期是当前会话，意思就是说，只要当前浏览器还没有关闭，就算当前页面关闭或者其他跳转到其他页面，再次回到该页面，cookie 还是保存着的，当前会话是指浏览器的当前会话，浏览器的当前会话只有在关闭浏览器之后才会被清除，如果想做一个记住我的功能，对浏览器的cookies 要做一个长期的存储的，保存时间就不能只是当前会话了。

接下来上大招，flask_login ，看一下高端的写法应该怎么玩。

## flask-login 的 session

flask_login 还是万变不离其宗，更加直接，将 user_id 写入 session，session 里面找有 user_id 就是登陆的，flask_principal
 权限控制管理则是将 identity_id 写入 session，然后加密放在 cookie 里面。

至于 remember_me 功能就更简单了，将 user_id 放到了另一条 cookie 里，即未加密的数据，然后放一个加密的数据作为签名，cookie 的有效期设置为一年，在一年内使用的时候直接做签名校验即可，如果签名通过，就使用该 user_id 登录。

> 这里使用的是单向签名算法，同样使用 `SECRET_KEY` 作为签名密钥，很奇怪为什么不适用加密算法，在使用的时候解密就好了，也不用直接存储明文数据。

奇怪，不知道为什么要直接放加密数据，这样感觉不太稳，虽然自己手动改了之后校验不通过，但是能够看到session的内容始终不太好。

flask_login 还有一个功能就是判断用户是否为密码登录的，还是使用保存的 cookie 登录的，就是在 session 中写入一个 `_fresh` 的键值对，如果是密码登录的，在使用 login_user 的时候在 session 中写入 `_fresh=True`，在使用 cookie 登录的时候会写入 `_fresh=False`。

flask_login 在 session 中还写入了一个 `_id` 的字段，不知道有什么用，好像是没有看到使用的，只有在密码登录的时候才会有这个字段，好像是用户浏览器的唯一标志，即将浏览器的 user-agent 和 IP 做了一个 sha512 哈希之后的数据，保存在 session 中，使用 cookie 登录的就没有。

flask_login 无法控制 SessionInterface ，即不能控制 session 的形式和存储状态等，只能在 session 中存内容，在 login_user 时将 `user_id` ,`_fresh`, `_id`, `remember` 等写入,在当前请求的栈顶推入登入的用户 `current_user`，在当前请求中使用 `current_user` 可以获得当前登录的用户。在 flask_login 在 session 中写入数据之后，flask 的 process_handler 检测到 session 中有数据，调用 sessions.save_session 方法，将数据加密后存入 cookie 中。

所谓的得到当前session的意思只是得到该 session 中存储的用户数据而已，实际上这部分数据全部加密存储在 cookie 中。 
在写入 cookie 的时候，当前登录的用户信息作为一个 cookie 写入，用户的 remember 信息作为另一个 cookie 写入，flask_login 虽然不能控制 SessionInterface，在 save_session 时将session全部序列化写入cookie，但是可以在请求之后，注册一个 after_request 事件，在这个函数中将 session 中的 remember 信息单独作为一个 cookie 写入 response ，然后一起传给前端。这就说明 save_session 函数调用是在 after_request 之后。

```
app.after_request(self._update_remember_cookie)

def _update_remember_cookie(self, response):
    # Don't modify the session unless there's something to do.
    if 'remember' in session:
        operation = session.pop('remember', None)

        if operation == 'set' and 'user_id' in session:
            self._set_cookie(response)
        elif operation == 'clear':
            self._clear_cookie(response)

    return response

```

而且在 after_request 的函数中将 remember 的信息弹出了，怪不得后来使用登录时的 cookie 已经没有了 remember 字段。
在将remember信息存入 cookie 的方式非常的简单粗暴，就是将session中的user_id和 app.secret_key 作为密钥，sha512 哈希算法的 hmac 加密 user_id 一起存入cookie，确实不可解密，但是可以防篡改的验签。

在 flask_login 将 remember 信息存入 cookie 之后，flask 的 save_session 也要行动了，此时在 login_user 中被存入的 remember 字段已经被弹出了，只剩下 `_fresh`, `_id`, `user_id` 三个字段。

在 save_session 中，dumps 函数中一个 serializer ，一个 signature ，边序列化边签名，一起存入cookie，所以在 open_session 中 loads 一个反序列化，一个验签。

在请求到来之后，那 open_session 肯定也是 before_request 之前的了，将 cookie 中的 session 数据取出来，放到本次请求的全局变量 session 中去。

如果是请求受到 login_required 装饰的方法，就会去判断 current_user 是否授权，一般登录即存在，存在即授权，所以就是判断 current_user 是否存在，所以 current_user 是在什么时候在这次请求中被推入栈顶的呢？

> 有一个疑问，就像其他的 LocalProxy 导入的全局变量一样，current_user 都是只知道被引入了，但是不知道是在什么时候被引入的，在什么条件下触发的，是被谁调用的，最终反正就是得到了。在请求的开始的时候。

在 flask_login 中的 current_user 是将 `_get_user` 得到的 user 对象返回，而且它也能够在没有栈顶没有 user 对象的时候推入 user ，而这个 user 可以从 session 中取 user_id ，然后通过 login_manager.user_loader 来得到 user 对象，这是在用户登录的时候，也可以在用户使用 remember  cookie 信息登录的时候从 cookie 中得到，或者是从 HTTP header 中得到，或者是从请求参数中得到， 这几种方式在得到 user 之后就会将 user 信息导入 session 中。

Session 中的 remember 字段默认是没有的，或者默认为空，当其为 set 的时候就表明要设置 cookie 了，这是在使用了 remember=True 的 login_user 的时候，在设置 cookie 之后即被弹出，当其为 clear 时就表明要删除 cookie 了，这是在使用了 logout_user 的时候被设置的，在 logout_user 时栈顶的 user 也被弹出，current_user 变为 AnonymousUserMixin 。同样的，在 after_request 中，既然可以设置 cookie ，那么也就可以删除 cookie，在删除 remember 的cookie之后，session 中的 remember 字段也被删除。在 logout_user 中 `user_id`, `_fresh` 被删除，remember 字段被设置然后删除，remember 的 cookie 被删除，当前请求的栈顶 user 被弹出，在剩下 session 中的 `_id` 还依旧倔强的留在session中，所以最后，session 依旧作为 cookie 被一直返回给前端。

最后写一点，flask_login 的 session_mode 挺有意思，当其为 strong 的时候，session 中的 `_id` 就会派上用场了，如果当前 session 被使用在不用的浏览器和IP上，就会删除当前session和用户前端的cookie，这是很正确的，因为如果是正常用户的话，cookie无论怎么变都是在自己的电脑上，user-agent 无论如何不会改变，IP 的改变倒是有可能，就是在登录之后，切换IP了，就会被自动退出登录，那只需要再登录一遍就好了吖。本来用户切换 IP 了，就应该警觉一些，而如果没有切换 IP ，没有切换浏览器，应该 `_id` 也都是不会改变的，确实是有一定的安全性。

## flask-login 的 token

关于 flask_login 不知道是在进化还是在退化，竟然在 0.3.2 里面有一个很好用的 feature 在 0.4.0 里面去掉了，就是 token_loader,使用 token_loader 的话，需要在你的 UserMixin 的用户子类中实现 get_auth_token ，方法，这样就能在 remember 里面不要再直接放用户信息了，太危险了，就算是升级 session，将 session 变为 sid ，但是 remember 还是不能解决，因为是flask_login写入的，而不是我们能控制的，官方还非常贴心的提供了 make_secure_token 方法来安全的创建 token ，真的非常好用，来试一下，奇怪，为什么后面要去掉呢？

找来找去，终于在 changelog 里面找到 0.4.0 有提到，有老哥把 remember_me 当成 token 来使用，确实是人才吖，token 短小精悍，可长期持有，确实如果保留 token_loader 可以这样用，但是每次请求返回的时候会带上一个 cookie 的吖，但是这样用真的好么，明明有一个 request_loader 的吖，老哥。作者也是 real 耿直，直接就把这么好的 feature 给删了，让别人想用 remember 就必须存储那么丑的 session ，丑拒。

```
BREAKING: The `login_manager.token_handler` function, `get_auth_token` method
on the User class, and the `utils.make_secure_token` utility function have
been removed to prevent users from creating insecure auth implementations.
Use the `Alternative Tokens` example from the docs instead. #291
```

好像是[这位老哥](https://github.com/maxcountryman/flask-login/issues/160)

一个 remember cookie 可以被大量的，多次的使用，但是有一个问题就是，无论被使用多少遍，它的过期时间都不会改变，即不会给你生成一个新的 remember 信息，也不会延长 remember 的过期时间，确实挺合理的，remember 信息在重新登录之后，才会改变，生成一个新的，但是原来的那个还是有效的，可以用的，也没有刻意的去清之前的cookie，只是拿一个新的去覆盖原来的旧的。

## flask-login 的两种 token 实现方式

发现直接使用 session 加密当数据的一个重要缺陷，就是直接使用加密之后的 session ，无论有没有登出，或者后面做了什么操作，拿以前的有效期之内的 session 都是可以继续用的，包括 remember 信息。虽然在操作时都会将前端的cookie做一个清理，或者说每一次cookie都会改变，但是使用之前的 cookie 终究是不稳吖，但是使用 sid 就很稳了，因为每一次从缓存中读取之后，就会将前一个 sid 删掉，只读一次。这就很好的嘛。

实际上 session 保存的实质一个字典的信息，登入状态只是有没有 current_user ，当前有没有用户，在栈顶有用户，即登录，没有，则未登录。session 和 current_user 并不是绝对的相互对应，有 session，或许只是有保存信息，并不一定有用户，有用户，也并不一定需要一个 session 。

flask-login 的两种 token 实现方式，一种是 session_token ，在 SessionInterface 中的读取 session 和写入 session 的时候，不再是从 cookie 中读取，而是从 header 里面读取 session 。还有一种方式是使用 flask-login 提供的 request_loader ，可以从 header 或者请求参数中读取 token

session_token 和 login_token 都能够实现 token 的功能，在 session_token 中 token 还可以当做 sid 使用，但是当成 sid 只能使用一次，就会失效了，需要使用返回的新的 sid ，在是 login_token 中 token 不仅可以放在 header 中，还可以放在 URL 请求参数中，效果一致。

Token 是能够多次使用的，使用后不会变的，再次生成原来的不受影响，session_login 且能够登出，即 token 失效，在 login_session 中不能登出。session_token 的使用期限在每次登录后缓存刷新，理论可以一直长久的无限使用，login_token 的有效期是固定值的，缓存失效需要再次登录，获得新的 token。

## 多点登录，任意下线

Flask-redis 真实坑吖，flask-cache 设置缓存为 redis 的时候存进去str，取出来 str ，但是 flask-Redis，存进去 str ，取出来 bytes，python 3 中。
