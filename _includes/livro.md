
## Mês das almas do Purgatório

Meditações práticas para cada dia do mês de novembro


### Capítulos

<ul id="chapter-list">
{% for chapter in site.book %}
  <li data-day="{{ chapter.order }}">
    {% assign order_int = chapter.order | plus: 0 %}<a href="{{ chapter.url | relative_url }}">{% if order_int >= 1 and order_int <= 30 %}{{ chapter.order }} &ndash; {% endif %}{{ chapter.title }}</a>
  </li>
{% endfor %}
</ul>

### Livro traduzido


Baixe o arquivo [PDF]({{ '/book/src/content/main.pdf' | relative_url }}) principal ou sua versão [compacta]({{ '/book/src/content/compact.pdf' | relative_url }}).


### Original

_Mois des ames du Purgatoire ou  
Méditations pratiques pour chaque jour du Mois de Novembre_  
Abbé Martin Berlioux.  
Vic et amat, cinquième édition, Paris, 1888.

Livro original em formato [PDF]({% link moisdesamesdupurgatoire.pdf %})  
Fonte: [The Internet Archive](https://archive.org/details/moisdesamesdupur00berl)
