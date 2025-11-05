---
layout: page
title: Privacidade
order: 5
sidebar: false
---

## Política de Privacidade

Este website usa _cookies_ para analisar tráfego ao site e melhorar a experiência do usuário.  
<!-- _This website uses cookies to analyze site traffic and improve user experience._ -->

### Que cookies usamos?

- **Google Analytics**: usamos _Google Analytics_ para entender como os visitantes interagem com as páginas do site. Esses _cookies_ coletam informação de forma anônima.
<!-- we use to understand how visitors interact with our website. These cookies collect information in an anonymous form. -->

### Como remover os cookies?

Você pode revogar o consentimento aos _cookies_ a qualquer momento limpando o cache do navegador ou clicando no botão abaixo.  
<!-- _You can revoke cookie consent at any time by clearing your browser's local storage for this site or by using the button below._ -->

<button onclick="revokeCookieConsent()" style="background: #f44336; color: white; border: none; padding: 0.5rem 1rem; cursor: pointer;">Revogar consentimento ao _cookie_</button>

<script>
function revokeCookieConsent() {
  localStorage.removeItem('cookieConsent');
  document.cookie = '_ga=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
  document.cookie = '_gid=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
  document.cookie = '_gat=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
  alert('Consentimento ao cookie revogado. Esta página irá carregar novamente.');
  location.reload();
}
</script>
