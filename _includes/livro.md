
## Mês das almas do Purgatório

Meditações práticas para cada dia do mês de novembro


### Capítulos

<ul id="chapter-list">
{% for chapter in site.book %}
  <li data-day="{{ chapter.order }}" style="display: none">
    <a href="{{ chapter.url | relative_url }}">{{ chapter.order }}</a> &ndash; <a href="{{ chapter.url | relative_url }}">{{ chapter.title }}</a>
  </li>
{% endfor %}
</ul>


### Original

_Mois des ames du Purgatoire ou  
Méditations pratiques pour chaque jour du Mois de Novembre_  
Abbé Martin Berlioux.  
Vic et amat, cinquième édition, Paris, 1888.

Livro original em formato [PDF]({% link moisdesamesdupurgatoire.pdf %})  
Fonte: [The Internet Archive](https://archive.org/details/moisdesamesdupur00berl)

<script>
const today = new Date();
const elements = document.querySelectorAll('li[data-day]');

elements.forEach(li => {
  // Get the day value from the attribute
  const dayValue = parseInt(li.dataset.day);
  
  // Check if it's a valid day number
  if (!isNaN(dayValue) && dayValue >= 1 && dayValue <= 30) {
    // Create the comparison date (2025-11-DD)
    const comparisonDate = new Date(2025, 10, dayValue); // Month 10 = November (0-indexed)
    
    // Show or hide based on comparison
    if (today >= comparisonDate) {
      li.style.display = ''; // Show (restore default display)
    } else {
      li.style.display = 'none'; // Hide
    }
  }
});
</script>