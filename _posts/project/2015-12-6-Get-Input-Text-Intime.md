---
layout: post
title: 实时获得输入表单的值
category: project
description: 有时候我们需要实时的得到输入表单的值，并用其他的形式表现出来。
---

假设我们有两个textarea，一个用来表单输入，一个用来实时展现输入的内容。     

刚开始我准备用`onChange`结果发现这个对表单输入的检查是在失去焦点之后的，就是说在失去焦点才对表单进行检查，如果内容改变才触发。                  

接着找，还有`onpropertychange`，但是网上说它是IE专用的，结果我自己测试什么结果都没有。。。  

终于找到了`oninput`，这个才是货真价实的表单输入改变即触发的事件。网上说不支持Firefox，结果我用Firefox，Opera，chrome，edge亲测都支持的非常好。

为什么会这样，网上说的都是骗人的，乖乖用`oninput`就好。       
不过网上还说了一个替代的办法，就是定时检测输入表单的变化，想了一下理论上是可行的，但是这样的话会不会太浪费了，每秒钟或者多久检查一次。         

代码如下：                            

```html
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Textarea</title>
	<script>
	window.onload = function(){
		document.getElementById("text").oninput = function(){
			result = document.getElementById("text").value;
			document.getElementById("result").value=result;
		}
	}

	</script>
</head>
<body>
	<div>
		<textarea name="name" id="text" cols="30" rows="10"></textarea>
		<textarea name="result" id="result" cols="30" rows="10"></textarea>
	</div>
</body>
</html>
```
