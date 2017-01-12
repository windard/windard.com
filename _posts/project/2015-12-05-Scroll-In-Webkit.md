---
layout: post
title: 重新设计你的滚动条
category: project
description: 现在都已经是在二十一世纪，可是原生的滚动条还是像上个世纪的产物一样，现在，就让我们自己动手来重新设计好看的滚动条吧。
---

## 滚动条从哪里来
一般滚动条会出现的地方就是该区域包含的内容超出规定的大小就会出现滚动条。                   
比如说：               
- 浏览器边框                    
- `textarea` 
- `iframe`   
- `div`或者是任何`block`元素，当他们的大小固定且`overflow`设定为`auto`或者是`scroll`的时候 

## 先看一下原生的滚动条
我们的代码是这样的，只有一个`div`，大量的内容并设定`div`的高和宽，然后设定`overflow:scroll` 

```html
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Beautiflu_scroll</title>
	<style>
	*{
		margin:0;
		padding:0;
	}
	.content{
		width:200px;
		margin:50px auto 0;
		height: 200px;
		overflow: scroll; 
	}
	</style>
</head>
<body>
	<div class="content">
	    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur rhoncus tortor eget orci fringilla non semper magna aliquet. Aliquam convallis elit sem. Proin fringilla fermentum pretium. Phasellus id nisl eu eros convallis eleifend. In hac habitasse platea dictumst. In at felis massa. Maecenas vitae quam non elit porta pellentesque ac in erat. Nullam a ante felis, ullamcorper suscipit felis. Maecenas sit amet nisl mattis ipsum ullamcorper aliquam vitae sed sapien. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.</p>

	    <p>Sed sed tellus dolor, non lobortis felis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. In eget nisl viverra risus feugiat vulputate tempus et leo. Nam metus nibh, tristique non sodales non, interdum et neque. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed imperdiet aliquet vestibulum. Curabitur viverra tortor augue, a aliquet tellus. Vivamus eu felis vel lorem tincidunt imperdiet. Fusce iaculis luctus convallis. Proin adipiscing malesuada enim, et feugiat tortor sagittis eu. Cras convallis felis eu leo tempus et fermentum urna accumsan. In quis metus at metus ultricies fringilla. Maecenas sed lacus aliquam nibh semper dignissim et quis est.</p>
	    
	    <p>Praesent sodales, sapien sit amet congue egestas, sem ligula ornare massa, vitae suscipit felis ligula quis velit. Phasellus lectus massa, sodales ac vulputate ac, pharetra quis lacus. Morbi tempus pretium nisi sed pretium. Pellentesque dictum volutpat vulputate. Fusce dapibus sagittis felis, ut consequat nisi posuere id. Cras elit orci, vehicula in sagittis a, faucibus vitae dui. Nunc non lorem in metus adipiscing adipiscing non a sapien. Sed dictum ultrices nibh in tristique. Nulla dapibus laoreet tincidunt. Sed accumsan erat quis mi luctus porta.</p>

	    <p>Sed mollis justo enim, ut pharetra nunc. Fusce vehicula viverra magna, et fringilla lectus porta quis. Donec eu fermentum mi. Donec congue pellentesque iaculis. Phasellus est leo, cursus eget consectetur in, tristique sit amet tortor. Cras eleifend felis sit amet eros vehicula aliquet. Pellentesque fringilla metus in libero luctus eu condimentum nulla pretium. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam consequat sodales lorem, nec dignissim turpis pharetra et. Nullam commodo hendrerit elementum. Donec porta faucibus ligula non blandit. In ultrices vehicula pretium.</p>

	    <p>Sed ac sagittis sapien. Curabitur varius pellentesque nunc eget molestie. Vivamus in massa arcu, ut auctor tellus. Aliquam convallis lobortis magna, ut posuere odio euismod ac. Vestibulum in enim vitae metus vulputate interdum. Mauris a risus auctor nunc fermentum dapibus. Proin iaculis, nunc ut viverra varius, augue augue porta libero, id viverra nisl elit in mauris. Aenean quis risus ante. Donec bibendum erat a sem vestibulum eu aliquet lectus tincidunt. Vivamus imperdiet congue leo, non ultricies urna sodales sed. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nulla vitae rhoncus dui. Nunc in nisi in ante imperdiet tincidunt sagittis eu ipsum. Aenean orci justo, faucibus placerat tincidunt vitae, vehicula at libero.</p>
		
	</div>
</body>
</html>
```

结果就是这样，在chrome 48.0上的样子。    

![beautiful_scroll_begin.jpg](/images/beautiful_scroll_begin.jpg)

## 开始用css美化滚动条
chrome浏览器在很多年之前就支持滚动条的css操作，但是非常可惜的是直到现在都没有指定一个统一的标准，所以我们在使用css属性时需要加上`-webkit-`浏览器前缀属性。                   
chrome支持的滚动条css属性有这些，属于css伪类。                    
1. -webkit-scrollbar  滚动条本身
2. -webkit-scrollbar-track  滚动条滑轨
3. -webkit-scrollbar-thumb  滚动条滑块
4. -webkit-scrollbar-button 滚动条两边按钮
5. -webkit-scrollbar-corner 横向滚动条和纵向滚动条相交处

我们来一些简单的示例，在页面css中加入以下代码。 

```css
	.content::-webkit-scrollbar{
		background-color: #97c0F6;
		width:5px;
		height:5px;
		border-radius: 2px;
	}
	.content::-webkit-scrollbar-thumb{
		background-color: #FFF88D;
	}
	.content::-webkit-scrollbar-corner{
		border-radius: 50%;
		background-color: #FF751B;
	}
	}
```

然后效果就是这样。     

![beautiful_scroll_decond.jpg](/images/beautiful_scroll_decond.jpg)

或者换成这样的代码。                      

```css
	.content::-webkit-scrollbar{
		width:20px;
		height:20px;
		background-color: #8F5252;
	}
	.content::-webkit-scrollbar-thumb{
		background-color: #7C2929;
	}
	.content::-webkit-scrollbar-button{
		background-color: #7C2929;
	}
	.content::-webkit-scrollbar-corner{
		background-color: #000;
	}
```

然后效果就是这样。    

![beautiful_scroll_decond_2.jpg](/images/beautiful_scroll_decond_2.jpg)

甚至你还可以这样，当鼠标移入div区域的时候才显示滚动条，否则滚动条消失。                 

```css
	.content::-webkit-scrollbar{
		width:0px;
		height:0px;
		background-color: #8F5252;
	}
	.content:hover::-webkit-scrollbar{
		width:20px;
	}
	.content::-webkit-scrollbar-thumb{
		background-color: #7C2929;
	}
	.content::-webkit-scrollbar-button{
		background-color: #7C2929;
	}
	.content::-webkit-scrollbar-corner{
		background-color: #000;
	}	
```

在你鼠标不在的时候不显示。只有当你的鼠标移入div区域的时候，滚动条才会显示。           

![beautiful_scroll_last.jpg](/images/beautiful_scroll_last.jpg)


## 其他的浏览器呢
以上的方法只有在`webkit`内核的浏览器上才有用，但是其他的浏览器支持的情况怎么样吖？
非常神奇IE竟然也支持滚动条的css属性，不过只能改变颜色，而且非常神奇的是，IE支持竟然eage不支持。。。                     
IE的滚动条分别有以下属性，这次不再是伪类了，而是实实在在的css属性。
1. scrollbar-face-color 滚动条滑块的颜色
2. scrollbar-arrow-color 滚动条两边三角箭头的颜色
3. scrollbar-highlight-color 滚动条滑轨的颜色
4. scrollbar-base-color    滚动条的基本颜色
5. scrollbar-3dlight-color 滚动条滑块3D效果的颜色
6. scrollbar-shadow-color  滚动条滑块阴影效果的颜色
7. scrollbar-track-color   滚动条滑轨的颜色
8. scrollbar-darkshadow-color 滚动条滑块阴影的颜色

实例代码，在css中加入以下代码：

```
	.content{
		 scrollbar-base-color:#000;
		 scrollbar-arrow-color: #999;
	}
```

效果就是这样的。                       

![beautiful_scroll_ie.jpg](/images/beautiful_scroll_ie.jpg)

本人现在的博客的导航条效果是这样的

```
html::-webkit-scrollbar{
    width:8px;
    background-color:#ddd;
    transition: all ease-in-out 0.5s;
}
html::-webkit-scrollbar-thumb{
    background-color:#aaa;
    border-radius:3px;
}
```

还有其他的浏览器呢？？？                        
只能怪他们不争气了，没有css属性，那就只用用js插件了，有一个插件还不错的样子，[malihu-custom-scrollbar-plugin](https://github.com/malihu/malihu-custom-scrollbar-plugin)        



## 参考链接                                             
[用CSS美化你的滚动条](http://www.webhek.com/scrollbar)                  
[在css中定义滚动条样式](http://www.cnblogs.com/luluping/archive/2009/10/31/1593664.html)          