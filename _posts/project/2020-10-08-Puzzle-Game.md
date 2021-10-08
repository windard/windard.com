---
layout: post
title: 拼图游戏
description: 介绍两款比较有意思的拼图游戏，及其解法
category: project
---

## 缘起

在今年五月份得到的第一份拼图，看起来平平无奇，当时觉得也不是很难的样子。

![](https://windard-blog.oss-cn-beijing.aliyuncs.com/6271633685384_.pic.jpg)

然后拼了两个月，使用各种姿势都尝试过，都没有拼起来，甚至在怀疑这是个真的拼图么？还是一个故意没有解法的拼图，让你浪费时间。

但是看到其包装盒上写的是 `the most difficult of puzzle designs`, 无奈弃之一旁，再无瓜葛。

![](https://windard-blog.oss-cn-beijing.aliyuncs.com/6251633685382.jpg)

## 解决

这个拼图是真的很难的，根据拼图难度分级据说是十级难度，就是最高难度。九片拼图，十级难度。

因为它会给你很多误导，看起来很多种尝试都可以完美的结合在一起，但是实际上缺因小失大，和其他的分片不能兼容。

其中最难的是有一个直角边，看起来就是在某一个角的位置，十分的规则，结果竟然是最不规则的一个，直接斜着放入。

其实我一直都没有解决，在网上的一个视频上偶然发现了这个拼图的解法，对这个拼图顿时多了几分敬意。

respect ！！！

![](https://windard-blog.oss-cn-beijing.aliyuncs.com/6261633685383_.pic.jpg)

终于，在得到这个拼图五个月后，第一次完整的拼起来。

![](https://windard-blog.oss-cn-beijing.aliyuncs.com/6281633685384.jpg)

泪目，✿✿ヽ(°▽°)ノ✿ 完结撒花。

## 日历

一般的拼图游戏，或者其他的益智解谜类游戏，无论过程是多么的辛苦，一路经过多少的挫折，花了多长的时间。

一但完成之后就会立刻变得索然无味，因为再次实现就会非常的简单。

![](https://windard-blog.oss-cn-beijing.aliyuncs.com/uTools_1633685451818.png)

但是这款日历拼图就不一样，它能够让你一年之内都爱不释手，每天一个新的挑战。

![](https://windard-blog.oss-cn-beijing.aliyuncs.com/6231633685380_.jpg)

![](https://windard-blog.oss-cn-beijing.aliyuncs.com/6311633686693.jpg)

【A Puzzle A Day】

## 解法

这款日历拼图其实并不难，一般十几分钟都能解决，但有的时候就是拼不出来，十分难受，憋屈的很，心慌意乱，然后就会花更长的时间。

有一个[在线地址](https://x6ud.gitee.io/a-puzzle-a-day/#/)，可以试玩一下。

![](https://windard-blog.oss-cn-beijing.aliyuncs.com/uTools_1633687942096.png)

然后刚开始拼起来还挺好玩的，每天都有一个小小的成就感，但是真的需要耐心，性子急的人不适合。

不然就是一天一个拼图，一个拼图拼一天。A Puzzle A Day，A Day For A Puzzle。

国庆节七天果然一天都没拼出来，气死我了，😤，气死我了，😡。

不就是拼图嘛，我写代码解一个，暴力遍历，递归加回溯，实现 [OnePuzzle](https://github.com/windard/OnePuzzle)。

![](https://windard-blog.oss-cn-beijing.aliyuncs.com/uTools_1633677947082.png)

可以解出来任意天的日历拼图，虽然时间也有长有短，但是比手动还是要快了不少，我又快乐了，哈哈，😄。

使用也很简单，直接 `pip install OnePuzzle` 即可安装。

然后使用 `one_puzzle` 命令就可以自动解图了，比如 `one_puzzle 10 11` 就会给你10月11日的一个解法。

加上 `-d` 参数就会展示计算次数，一般都需要经过几十万甚至上千万次计算才能够有一个合适的解，计算机还是快吖。

加上 `-a` 参数就会计算所有的解法，因为代码问题，或者算法问题，现在这里的计算还是需要很长很长时间的，可以后续优化一波。😂

其实一开始我就知道，有一个在线解法，[Calendar Puzzle Solver](https://joinker.oss-cn-shanghai.aliyuncs.com/calendar-puzzle-solver/index.html),它能够根据当前日期，得到当天解法，而且只有当天的解法。

![](https://windard-blog.oss-cn-beijing.aliyuncs.com/screenshot-20211008-181305.png)

这样其实挺好的，每次只给当天的解法，这一天的全部解法，🐂🍺。
