---
layout: post
title: 创建局域网并实现局域网通信
category: project
description: 主要通过有线或无线的方式创建局域网，然后测试一下本人的Python的局域网通信工具
---

局域网通信是一个很有用的东西，不走Internet，试一下搭建一个局域网，在局域网里通信试试。

## Windows上搭建局域网

### 有线

#### 路由器
将电脑连接网线，网线的另一头插入路由器的LAN口，一般情况下路由器会自动分配IP，可以在路由器后台管理页面查看，或者在cmd窗口用ipconfig命令查看。

路由器的WAN口接入Internet或者不接入，插入LAN口的几台电脑都可以创建局域网。

此法一般用于多台电脑。

如果真的有的路由器并没有分配IP，这样的话就需要手动的给每台电脑设置IP地址了，需要设置的IP地址在同一网段。

#### 直接连网线
使用一根网线将两台电脑连接起来，即网线的一头连接一台电脑。

一般这样连接起来两台电脑也会自动分配IP地址，但是这样的话，两台电脑的IP一般不在一个网段，如果想要构成局域网，必须两台电脑的IP在同一网段。

>两台电脑的IP在同一网段的意思是两个IP地址除了最后一段不一样，其他的都一样。比如说192.168.0.100与192.168.0.101就是在同一网段，192.168.1.100与192.168.137.101就不是在同一网段。

当然也有可能两台电脑的IP在同一网段，就可以不用设置了。

如果不在同一网段的话，就需要设定一下IP地址。因为正常情况下电脑的IP地址是动态分配的，也就是说，在连接之前不是不能确定它的IP地址的，那么为了方便，我们将两台电脑的IP地址全部设为静止IP。

这是我的动态分配的IP地址。

![ipconfig_raw](/images/ipconfig_raw.JPG)

那么在哪里将电脑的IP地址设为静止IP呢？
右击[开始]，点击[控制面板]，点击[查看网络状态和任务]，点击[更改适配器设置]，找到你的[以太网]连接。 

![control_canel.png](/images/control_canel.png)

![chack_interect.png](/images/chack_interect.png)

![change_config.png](/images/change_config.png)

![eth0_connect.png](/images/eth0_connect.png)

右击，选择[属性]，找到ipv4，双击这一选项。

![change_set.png](/images/change_set.png)

![changeipv4.png](/images/changeipv4.png)

![ipv4_setting.png](/images/ipv4_setting.png)

改为使用下面的IP地址，并设IP地址为一个合适的值，如192.168.0.100，设子网掩码为一个合适的值，如255.255.255.0，然后保存更改。

![ipv4_changed.png](/images/ipv4_changed.png)

使用ipconfig，查看IP地址。
![ipv4_changed_cmd.png](/images/ipv4_changed_cmd.png)


然后同样的步骤将另一台电脑的IP地址也设为一个合适的值，如192.168.0.101。现在，两台电脑就都在同一个局域网内了。它们的IP地址就是设定的值。

### 无线

#### WiFi热点工具
猎豹WiFi或者是360免费WiFi都可以，打开热点，其他的电脑连接这个WiFi，即相当于几台电脑都在一个局域网内。同样的电脑有无Internet连接都可以。

#### 手工创建WiFi热点

1. 打开cmd              

2. netsh wlan set hostednetwork mode=allow                 

3. netsh wlan set hostednetwork ssid=wifiname key=wifipassword（密码长度必须大于等于8）

4. netsh wlan start hostednetwork

5. 进入[网络连接]->[更改适配器设置] 选择一个可用网络将其共享到Microsoft Virtual wlan Miniport Adapter                    

![share_internet.png](/images/share_internet.png)             

7. 其他电脑连接你的WiFi，即创建局域网             
>查看WiFi连接状况：netsh wlan show hostednetwork

这样的话要求自身的电脑必须先连接Internet然后才能创建WiFi。


