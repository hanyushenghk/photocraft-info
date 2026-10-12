/* Keep desktop and mobile navigation in sync with routes and home anchors. */
(() => {
 const links = [...document.querySelectorAll('.topbar .navlinks a, .topbar .mobile-nav a')];
 const route = path => path.replace(/^\/(zh|en)(?=\/|$)/, '').replace(/\/+$/, '') || '/';
 function update() {
  const path = route(location.pathname);
  let section = null;
  if (path === '/') {
   if (['#compare', '#community'].includes(location.hash)) section = location.hash;
  } else {
   section = ['plugins', 'templates', 'download'].find(key => path === '/' + key || path.startsWith('/' + key + '/')) || 'guides';
  }
  links.forEach(link => {
   const url = new URL(link.href, location.href);
   const target = route(url.pathname);
   const active = section && (section.startsWith('#') ? target === '/' && url.hash === section : target === '/' + section && !url.hash);
   if (active) link.setAttribute('aria-current', section.startsWith('#') ? 'location' : 'page');
   else link.removeAttribute('aria-current');
  });
 }
 // Full page links stay independent of the current home section/hash.
 links.forEach(link => link.addEventListener('click', event => {
  if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || link.target === '_blank') return;
  const target = new URL(link.href, location.href);
  if (target.origin !== location.origin || target.pathname === location.pathname) return;
  event.preventDefault();
  location.assign(target.href);
 }));
 update();
 window.addEventListener('hashchange', update);
 window.addEventListener('popstate', update);
})();
