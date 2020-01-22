---
layout: page
title: News
---

Please do note that even if the title or the description of the post is only in Finnish, most of them do also have the English text in them.

{% include functions/archive-navi_en.html %}

<div class="flex-container">
  <div class="flex-item">
      <h2>Main news</h2>
      {% assign main_category_posts = site.categories[site.main_category] %}
      {%
        include functions/post-list_en.html
        posts=main_category_posts
        category_links=true
      %}
  </div>

  <div class="flex-item">
      <h2>Other news</h2>
      {%
        include functions/post-list_en.html
        posts=site.posts
        category_links=true
        exclude_category=site.main_category
      %}
  </div>
</div>
