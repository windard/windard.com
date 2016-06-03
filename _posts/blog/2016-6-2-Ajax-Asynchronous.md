---
layout: post
title: Ajax 的异步与同步
description: Ajax 的全称是 Asynchronous JavaScript and XML ， 它本身是与浏览器的请求异步的，意思在正常页面加载完成之后再向服务器发出新的请求，但是在我们这里讨论的是在 javascript 执行的时候 Ajax 请求与其他 javascript 语句的执行情况，这里可以是同步的或异步的。
category: blog
---

## Ajax
Ajax 是一种在无需重新加载整个页面的情况下，能够更新部分网页的技术。传统的网页，如果需要更新内容，必须重载整个页面。这样的话有时只是需要部分数据的更新就需要发送大量的重复的请求，用户体验十分不友好。而使用 Ajax 技术，可以在不用刷新当前页面的情况下向服务器发出新的请求并获得数据，然后实时的在前端更新。这无疑是网页技术的一个必然的发展趋势，现在已经有的站点能够在整站使用 Ajax 技术，使用户停留在一个页面就能够完成所有的操作。

使用原生的 javascript 来实现 Ajax 请求比较复杂，现在一般使用 jQuery ，因为它已经把底层的浏览器兼容性问题为我们解决了，使用起来也比较方便。

在 JQuery 中关于 Ajax 的主要有六个函数，分别是 `jQuery.ajax(url[,setting])` , `load(url[,data][,callback])` , `jQuery.get(url[,data][,callback][,type])` `jQuery.getJSON(url[,data][,callback])` , `jQuery.getScript(url[,callback])` 和 `jQuery.post(url[,data][,callback][,type])` 。

## 同步和异步
前面已经说到，Ajax 本身是与浏览器的正常请求异步的，但是在 javascript 脚本执行过程中，它可以是异步的也可以是同步的，默认也是异步的。也就是说，在一个 Ajax 请求发出之后，javascript 执行线程是会跳过 Ajax 的部分，继续向下执行的，如果你需要用 Ajax 的返回值的话，那就只能在 Ajax 的返回函数里执行了，而如果想在 Ajax 之后使用 Ajax 的返回值，在异步的状态下一般只会得到 `undefined` 。

还有，如果你想同时执行两个或多个 Ajax 请求，在不同的浏览器里的可以同步执行的 Ajax 数目不一定，但是这样是可以的，开启多个不同的线程。只不过，在服务器端，如果你使用了 `session` 来判断用户身份的话，它会默认为每一次登陆状态分配一个独一无二的 `sessionid` ,在 Ajax 请求时，它会自动带上这个 `sessionid` ，不过如果你的多个 Ajax 同时请求带有同样的 `sessionid` 的话，php 只会认取第一个 `sessionid` ，也就是说多个 Ajax 请求在 php 看来只有第一个是有效的。

## 何时使用同步或异步
在 jQuery 的六个常用函数中，都是默认异步的，如果我们有时需要同时发送大量的 Ajax 请求，在 php 后端可能会出现一定的问题，这个时候就要使用同步，阻塞后面的 Ajax 执行。

其实在很多时候，我们并不是需要 Ajax 的同时执行，我们也可以在前一个 Ajax 的回调函数中执行下一个 Ajax 请求。
