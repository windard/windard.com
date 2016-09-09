---
layout: post
title: 两道前端的题目
category: project
description: 网上看到的自己写了一下，还是蛮好玩的。
---

##据说是前端笔试的题目，我也来试下。 

####题目如下
1. 第一道              
效果图如下。重点：中间的方框的大小是250*250，但是是在屏幕上水平垂直都居中的，然后就是那些小方块的大小是中间方块的50%，依次递减，准确的向四个角延伸。      
![work_1.jpg](/images/work_1.jpg)

2. 第二道             
效果图如下。重点：中间的四张图片还是水平垂直居中的，相互水平对其。然后上下的文字高度自适应。       
![work_2.jpg](/images/work_2.jpg)

3. 第三道        
然后其实第三道是我自己没事写的一个效果。效果图如下。重点：四个方块其实不是正方形，但是它们间距相等，而它们一起与左右边框距离相等，中间的一行文字水平垂直居中。           
![work_3.jpg](/images/work_3.jpg) 


####代码如下
1. 第一题：  

```html
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>work1</title>
	<style>
	*{
		margin:0;
		padding:0;
	}
	.center{
		margin:auto;
		position: absolute;
		top:0;
		bottom:0;
		left: 0;
		right:0;
		width:250px;
		height:250px;
		background-color:red;
	}
	.center div{
		width:50%;
		height:50%;
		background-color: red;
		position: absolute;
	}
	.one{
		top:-50%;
		left:-50%;
	}
	.two{
		top:-50%;
		right:-50%;
	}
	.three{
		bottom:-50%;
		left:-50%;
	}
	.four{
		bottom:-50%;
		right:-50%;
	}
	</style>
</head>
<body>
	<div class="center">
		<div class="one">
			<div class="one"><div class="one"><div class="one"></div></div></div>
		</div>
		<div class="two">
			<div class="two"><div class="two"><div class="two"></div></div></div>
		</div>
		<div class="three">
			<div class="three"><div class="three"><div class="three"></div></div></div>
		</div>
		<div class="four">
			<div class="four"><div class="four"><div class="four"></div></div></div>
		</div>
	</div>
</body>
</html>
```

2. 第二题：

```html
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>work2</title>
	<style>
	*{
		margin:0px;
		padding:0px;
	}
	.slide{
		float: left;
		width:25%;
	}
	.pic{
		width:250px;
		margin:0 auto 0;
		position: relative;
	}
	.center{
		text-align: center;
		width:1100px;
		position: absolute;
		top:50%;
		left:50%;
		margin-left: -550px;
		margin-top: -100px;
	}
	img{
		max-width: 100%;
		max-height: 100%;
	}
	.work{
		float: left;
		width:100%;
		text-align: left;
		position: absolute;
		bottom:100%;
		background-color: #ccc;
	}
	.under{
		float: left;
		width:100%;
		text-align: left;
		position: absolute;
		top:100%;
		background-color: #ccc;
	}	
	</style>
</head>
<body>
	<div class="center">
		<div class="slide"><div class="pic"><div class="work">这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。</div><img src="pic.jpg" alt="#"><div class="under">这里有一些文字。</div></div></div>
		<div class="slide"><div class="pic"><div class="work">这里有一些文字。</div><img src="pic.jpg" alt="#"><div class="under">这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。</div></div></div>
		<div class="slide"><div class="pic"><div class="work">这里有一些文字。这里有一些文字。这里有一些文字。</div><img src="pic.jpg" alt="#"><div class="under">这里有一些文字。这里有一些文字。</div></div></div>
		<div class="slide"><div class="pic"><div class="work">这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。</div><img src="pic.jpg" alt="#"><div class="under">这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。这里有一些文字。</div></div></div>		
	</div>
</body>
</html>
```

3.  第三题：

```html
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=Edge，chrome=1">
	<title>Document</title>
	<style>
	@media (max-width: 766px) {
	.one_item_box_box{
		width: 100%;
		padding: 20px 0;
	}		
	}		
	@media (min-width: 767px ){
	.one_item_box_box{
		width: 100%;
		padding: 40px 0;
	}
	}
	@media (min-width: 1200px) {
	.one_item_box_box{
		width: 100%;
		padding: 70px 0;
	}		
	}
	*{
		padding: 0;
		margin: 0;
	}
	a{
		color:white;
		text-decoration: none;
	}
	.one{
		max-width: 100%;
		overflow: hidden;
		padding: 20px 50px 20px;
	}
	.one_item{
		float: left;
		text-align: center;
		width: 16.6%;
		display: block;
		overflow: hidden;
	}
	.one_item_box{
		width: 80%;
		margin:0 auto 0;
		background-color: #000;
	}
	</style>
</head>
<body>
	<div class="one">
		<a href="#" class="one_item">
			<div class="one_item_box"><div class="one_item_box_box"><span>教务处</span></div></div>
		</a>
		<a href="#" class="one_item">
			<div class="one_item_box"><div class="one_item_box_box"><span>教务处</span></div></div>
		</a>
		<a href="#" class="one_item">
			<div class="one_item_box"><div class="one_item_box_box"><span>教务处</span></div></div>
		</a>
		<a href="#" class="one_item">
			<div class="one_item_box"><div class="one_item_box_box"><span>教务处</span></div></div>
		</a>
		<a href="#" class="one_item">
			<div class="one_item_box"><div class="one_item_box_box"><span>教务处</span></div></div>
		</a>
		<a href="#" class="one_item">
			<div class="one_item_box"><div class="one_item_box_box"><span>教务处</span></div></div>
		</a>
	</div>
</body>
</html>
```

####参考链接：
[有趣的前端题目，看了不后悔](http://blog.csdn.net/minidrupal/article/details/38681155)