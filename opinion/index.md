---
layout: home
---

<div class="index-content opinion">
    <div class="section">
        <ul class="artical-cate">
            <li><a href="/"><span>Blog</span></a></li>
            <li class="on" style="text-align:center"><a href="/opinion"><span>Opinion</span></a></li>
            <li style="text-align:right"><a href="/project"><span>Project</span></a></li>
        </ul>

        <div class="cate-bar"><span id="cateBar"></span></div>

        <ul class="artical-list">
        {% for post in site.categories.opinion %}
            <li>
                <h2>
                    <a href="{{ post.url }}">{{ post.title }}</a>
                </h2>
                <div class="title-desc">{{ post.description }}</div>
            </li>
        {% endfor %}
        </ul>
    </div>
    <div class="aside">
		<img src="../images/headlogo.jpg" alt="headlogo" style="width:50%;margin-top:15%">		
		<p>杨文强</p>
		<p>喜欢编程，热爱运动，爱好创造新的东西</p>
		<p>在这场人生新的旅行中，愿你我安好，万世太平</p>
	<div class="contact" style="margin-top:10%">
		<h4>You can find me on <a href="http://www.github.com/1106911190">Github</a><br />Or QQ:1106911190</h4>

	</div>
	<div class="copyright" style="margin-top:20%">
		<p><h5 style="font-family:arial;">Copyright &nbsp;&copy;&nbsp;2015 All rights reserved</h5>
			<h5>Powerd By <a href="https://github.com/jekyll/jekyll">Jekyll</a></h5>
		</p>
	</div>		

    </div>
</div>

<a href="http://github.com/1106911190"><img id="github_url"  style="position: absolute; top: 0; right: 0; border: 0;" src="http://s3.amazonaws.com/github/ribbons/forkme_right_red_aa0000.png" alt="Fork me on GitHub" /></a>
