const menu=document.querySelector('.menubtn');
if(menu){menu.addEventListener('click',()=>{const expanded=menu.getAttribute('aria-expanded')==='true';menu.setAttribute('aria-expanded',String(!expanded));document.querySelector('#mobile-nav').classList.toggle('open',!expanded)})}
document.querySelectorAll('[data-language]').forEach(a=>a.addEventListener('click',()=>{try{localStorage.setItem('photocraft-language',a.dataset.language)}catch{}if(location.hash)a.href+=location.hash}));
const search=document.querySelector('#guide-search');
if(search){const cards=[...document.querySelectorAll('.guide-card')];search.addEventListener('input',()=>{const q=search.value.toLowerCase().trim();let count=0;for(const card of cards){const match=card.dataset.search.includes(q);card.hidden=!match;if(match)count++}document.querySelector('#guide-count').textContent=count;document.querySelector('#guide-empty').hidden=count!==0})}
