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
					<h5>{{ post.time }}</h5>
                </h2>
                <div class="title-desc">{{ post.description }}</div>
            </li>
        {% endfor %}
        </ul>
    </div>
    <div class="aside">
		<p>这是杨文强的有一个站点<p>
    </div>
</div>

<a href="http://github.com/mojombo"><img style="position: absolute; top: 0; right: 0; border: 0;" src="http://s3.amazonaws.com/github/ribbons/forkme_right_red_aa0000.png" alt="Fork me on GitHub" /></a>
