
## Mês das almas do Purgatório

Meditações práticas para cada dia do mês de novembro


### Capítulos

<ul id="chapter-list">
{% for chapter in site.book %}
  <li data-day="{{ chapter.order }}" style="display: none">
    {% assign order_int = chapter.order | plus: 0 %}<a href="{{ chapter.url | relative_url }}">{% if order_int >= 1 and order_int <= 30 %}{{ chapter.order }} &ndash; {% endif %}{{ chapter.title }}</a>
  </li>
{% endfor %}
</ul>

### Livro traduzido


Baixe o arquivo [PDF]({% link book/src/content/main.pdf %}) principal ou sua versão [compacta]({% link book/src/content/compact.pdf %}).


### Original

_Mois des ames du Purgatoire ou  
Méditations pratiques pour chaque jour du Mois de Novembre_  
Abbé Martin Berlioux.  
Vic et amat, cinquième édition, Paris, 1888.

Livro original em formato [PDF]({% link moisdesamesdupurgatoire.pdf %})  
Fonte: [The Internet Archive](https://archive.org/details/moisdesamesdupur00berl)


<script>
const today = new Date();
const year = 2025;
const elements = document.querySelectorAll('li[data-day]');

elements.forEach(li => {
  // Get the day value from the attribute
  const dayValue = parseInt(li.dataset.day);
  
  if (!isNaN(dayValue)) {
    if (dayValue < 1) { li.style.display = ''; return; }

    // Create the comparison date (YYYY-11-DD)
    const comparisonDate = new Date(year, 10, Math.min(30, dayValue)); // Month 10 = November (0-indexed)
    
    // Show or hide based on comparison
    if (today >= comparisonDate) {
      li.style.display = ''; // Show (restore default display)
    } else {
      li.style.display = 'none'; // Hide
    }
  }
});
</script>