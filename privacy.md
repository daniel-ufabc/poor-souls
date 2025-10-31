---
layout: page
title: Privacy Policy
order: 5
---

## Cookie Policy

This website uses cookies to analyze site traffic and improve user experience.

### What cookies do we use?

- **Google Analytics**: We use Google Analytics to understand how visitors interact with our website. These cookies collect information in an anonymous form.

### Managing cookies

You can revoke cookie consent at any time by clearing your browser's local storage for this site or by using the button below:

<button onclick="revokeCookieConsent()" style="background: #f44336; color: white; border: none; padding: 0.5rem 1rem; cursor: pointer;">Revoke Cookie Consent</button>

<script>
function revokeCookieConsent() {
  localStorage.removeItem('cookieConsent');
  document.cookie = '_ga=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
  document.cookie = '_gid=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
  document.cookie = '_gat=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
  alert('Cookie consent revoked. The page will reload.');
  location.reload();
}
</script>
