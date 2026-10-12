const menu=document.querySelector('.menubtn');
const navigation=document.querySelector('#mobile-nav');
if(menu&&navigation){
 const zh=document.documentElement.lang==='zh-CN';
 const setMenu=open=>{menu.setAttribute('aria-expanded',String(open));menu.setAttribute('aria-label',zh?(open?'收起导航':'展开导航'):(open?'Close menu':'Open menu'));navigation.classList.toggle('open',open)};
 menu.addEventListener('click',()=>setMenu(menu.getAttribute('aria-expanded')!=='true'));
 navigation.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setMenu(false)));
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.getAttribute('aria-expanded')==='true'){setMenu(false);menu.focus()}});
}
document.querySelectorAll('[data-language]').forEach(a=>a.addEventListener('click',()=>{try{localStorage.setItem('photocraft-language',a.dataset.language)}catch{}const target=new URL(a.href,location.href);target.hash=location.hash;a.href=target.href}));
const search=document.querySelector('#guide-search');
if(search){const cards=[...document.querySelectorAll('.guide-card')];search.addEventListener('input',()=>{const q=search.value.toLowerCase().trim();let count=0;for(const card of cards){const match=card.dataset.search.includes(q);card.hidden=!match;if(match)count++}document.querySelector('#guide-count').textContent=count;document.querySelector('#guide-empty').hidden=count!==0})}
const assetCards=[...document.querySelectorAll('.asset-card')];
if(assetCards.length){
 const filters=[...document.querySelectorAll('[data-resource-filter]')];
 const input=document.querySelector('#resource-search');let category='all';
 const apply=()=>{const q=input.value.trim().toLowerCase();let count=0;for(const card of assetCards){const show=(category==='all'||card.dataset.resourceKind===category)&&card.dataset.resourceSearch.includes(q);card.hidden=!show;if(show)count++}document.querySelector('#resource-count').textContent=count;document.querySelector('#resource-empty').hidden=count!==0;filters.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.resourceFilter===category)))};
 filters.forEach(b=>b.addEventListener('click',()=>{category=b.dataset.resourceFilter;apply()}));input.addEventListener('input',apply);
 const fromHash=()=>{if(location.hash==='#resources-luts'){category='lut';apply()}};window.addEventListener('hashchange',fromHash);fromHash();
}
