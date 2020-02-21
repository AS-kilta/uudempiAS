---
layout: page
title: Uutiset
permalink: /uutiset/
---

<div class="flex-container">
  <div class="flex-item">
      <h2>Pääuutiset</h2>
      {% assign main_category_posts = site.categories[site.main_category] %}
      {%
        include functions/post-list.html
        posts=main_category_posts
        category_links=true
        limit=10
      %}
  </div>

  <div class="flex-item">
      <h2>Muut uutiset</h2>
      {%
        include functions/post-list.html
        posts=site.posts
        category_links=true
        exclude_category=site.main_category
        limit=10
      %}
  </div>
</div>

{% include functions/archive-navi.html %}

