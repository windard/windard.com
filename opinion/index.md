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
        <div class="head" style="margin-top:15%">
        <img src="{{ site.url }}/images/headlogo.jpg" alt="headlogo" style="width:50%;margin-top:15%;margin-bottom:10%">     
        <p>但行好事，莫问前程</p>
        <p>愿你我安好，一世太平</p>
        </div>
    <div class="contact" style="margin-top:35%">
        <p>You can find me on <a href="http://www.github.com/1106911190">Github</a></p>
    </div>
    <div class="copyright" style="margin-top:-5%">
        <p><p style="font-family:arial;">Design With Love By <a href="http://windard.com">Windard</a></p>
        </p>
    </div>      

    </div>
</div>

<a href="http://github.com/1106911190" class="forkme"><img id="github_url"  style="position: absolute; top: 0; right: 0; border: 0;" src="http://s3.amazonaws.com/github/ribbons/forkme_right_red_aa0000.png" alt="Fork me on GitHub" /></a>
