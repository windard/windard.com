---
layout: archives
title: 文章归档
---

<p>好记性不如烂笔头，已经写了 <span id="count"></span>	篇博客，继续加油哦 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ↖(^ω^)↗</p>

<section class="posts" id="posts">
    {% for post in site.posts %}
        <div class="post">
            <h4 class="post-title">
                <a href="{{ post.url }}">{{ post.title }}</a>
            </h4>
            <p class="post-date">{{ post.date | date: '%Y-%m-%d'}}</p>
        </div>
    {% endfor %}
</section>
