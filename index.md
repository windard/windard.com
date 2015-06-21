---
layout: home
---

<div class="index-content blog">
    <div class="section">
        <ul class="artical-cate">
            <li class="on"><a href="/"><span>Blog</span></a></li>
            <li style="text-align:center"><a href="/opinion"><span>Opinion</span></a></li>
            <li style="text-align:right"><a href="/project"><span>Project</span></a></li>
        </ul>

        <div class="cate-bar"><span id="cateBar"></span></div>

        <ul class="artical-list">
        {% for post in site.categories.blog %}
            <li>
                <h2><a href="{{ post.url }}">{{ post.title }}</a></h2>
				<h5>{{ post.date }}</h5>
                <div class="title-desc">{{ post.description }}</div>
            </li>
        {% endfor %}
        </ul>
    </div>

    <div class="aside">
		<img src="images/headlogo.jpg" alt="headlogo" style="width:50%;margin-top:10%">		
		<p>杨文强</p>
		<p>喜欢编程，热爱运动，爱好创造新的东西</p>
		<p>在这场人生新的旅行中，愿你我安好，万世太平</p>
    </div>
</div>

<a href="http://github.com/1106911190"><img style="position: absolute; top: 0; right: 0; border: 0;" src="http://s3.amazonaws.com/github/ribbons/forkme_right_red_aa0000.png" alt="Fork me on GitHub" /></a>
