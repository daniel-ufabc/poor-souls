---
layout: page
title: Livro
order: 3
sidebar: true
---

{% capture included_content %}
  {% include livro.md %}
{% endcapture %}

{{ included_content | markdownify }}