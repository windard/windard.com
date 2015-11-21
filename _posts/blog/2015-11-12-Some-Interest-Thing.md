---
layout: post
title: 一些好玩的东西
description: 电脑玩多了，总会越来越溜的~~~
category: blog
---

##以下包括本人玩电脑以来发现的很多有用的小的零散的东西。

>仅作记录
>

1. cmd命令行里神奇的`tree`，可以显示出目录文件结构，就像这样。   
![tree_demo.jpg](../../images/tree_demo.jpg)   
不过只能显示文件夹，不能显示文件。    

2. 如果你的cmd开了快速编辑模式的话，就可以直接将其拷贝出来，而且就可以在cmd里右击直接粘贴了，再也不用小心翼翼的敲命令了。  
![cmd_edit.jpg](../../images/cmd_edit.jpg)   
把上面的目录结构拷贝出来就是这个样子的。   
```
C:\Users\dell\Desktop\theme>
├─Jekyll-HMFAYSAL-Theme
│  ├─assets
│  │  ├─css
│  │  ├─fonts
│  │  ├─js
│  │  │  ├─plugins
│  │  │  └─vendor
│  │  └─less
│  ├─images
│  ├─_includes
│  ├─_layouts
│  ├─_plugins
│  └─_posts
└─yusi
    ├─admin
    ├─ajax
    ├─cache
    ├─fonts
    ├─img
    │  ├─pic
    │  └─smilies
    ├─js
    ├─modules
    ├─pages
    └─widgets
```

3. 查看当前正在进行的进程。    
`tasklist/top`，查看当前系统进程，`tskill/kill`，杀死某个进程。    

4. 让cmd里显示utf-8的中文。
因为cmd本身无法显示utf-8的中文，只能显示GBK的中文。如果想要显示utf-8的中文的话，输入`chcp 65001`    
方可显示utf-8格式编码中文,输入`chcp 936`,仍然显示GBK的中文     
>如果cmd中仍然无法显示utf-8的中文，选择属性，改变字体为`Lucida Console`点阵字体。

5. Python的包管理工具pip，可以用`pip freeze`来查看安装了那些Python的库。

6. 有时候不得不需要下载一些百度文库里的东西，一般我是拒绝这样做的。因为我有大量的百度云搜索。   
>[http://www.kanbuchuan.com/so/](http://www.kanbuchuan.com/so/)     
>[http://kaopu.so/](http://kaopu.so/)
>[http://www.iwapan.com/](http://www.iwapan.com/)
>[http://www.panzz.com/](http://www.panzz.com/)
>[http://www.bdyunso.com/](http://www.bdyunso.com/)
>[http://www.pansou.com/](http://www.pansou.com/)
>[http://www.wangpansou.cn/](http://www.wangpansou.cn/)
>[http://pan.java1234.com/](http://pan.java1234.com/)
>[http://www.kanbuchuan.com/so/](http://www.kanbuchuan.com/so/)
>[http://www.daysou.com/](http://www.daysou.com/)
>[http://www.panc.cc/](http://www.panc.cc/)
>[http://www.baidu10.net/](http://www.baidu10.net/)
>[http://www.yiso.me/](http://www.yiso.me/)
>[http://so.xpan.me/index.html](http://so.xpan.me/index.html)
>[http://www.soupan.info/](http://www.soupan.info/)              
    
    好吧，就这些，一般都能够找到想要的资料，但是如果实在是没有找到而且在百度文库里发现了想要下载的却提示需要积分的时候，内心是崩溃的。        
这个时候，我们就需要这个了，[冰点文库](../software/iDocDown.rar)，输入百度文库的网址即可下载，自动下载转化为TXT和PDF格式，还是非常好用的。我的这个是免安装无广告版，之前我也在网上找到一个，又有广告又需要安装。。。。

7. 在Windows命令行上执行Linux命令，或许你需要--GetGnuWin32。     
 - 下载[GetGnuWin32-0.6.3](../software/GetGnuWin32-0.6.3.exe)，运行。       
 - 进入GetGnuWin32的安装目录，运行`download.bat`,它会自动从网上下载你需要的Linux命令。（可能需要很长时间）        
 - 运行`install.bat`，就可以在cmd上使用Linux命令了。        

8. 在cmd中查看某个命令的详细信息。`XXX /?`，比如说`find /?`。

9. 判别一个Python变量是不是一个对象。`isinstance(XXX,object)`

10. 强行终止Python程序，`sys.exit()`

11. 一些基本的vim设置。
```
syntax on                   " 自动语法高亮
colorscheme torte           "配置颜色方案
set number                  " 显示行号
set cursorline              " 突出显示当前行
set wildmenu                 "Turn on WiLd menu 在末行命令行敲tab键时会在状态栏显示选项
set whichwrap+=h,l          "Bbackspace and cursor keys wrap to 使指定的左右移动光标的键在行首或行尾可以移到前一行或者后一行
set shiftwidth=4            " 设定 << 和 >> 命令移动时的宽度为 4
set softtabstop=4           " 使得按退格键时可以一次删掉 4 个空格
set tabstop=4               " 设定 tab 长度为 4
set nobackup                " 覆盖文件时不备份
set autochdir               " 自动切换当前目录为当前文件所在的目录
```
