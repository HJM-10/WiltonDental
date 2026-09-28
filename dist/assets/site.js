(() => {
  'use strict';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const progress = document.createElement('div'); progress.className='scroll-progress'; progress.setAttribute('aria-hidden','true');document.body.prepend(progress);
  let scrollFrame = 0;
  function updateJourney() {
    const timeline=document.querySelector('#timeline');if(!timeline)return;
    const steps=[...timeline.querySelectorAll('.journey-step')];
    const first=steps[0].querySelector('.step-dot').getBoundingClientRect();
    const last=steps.at(-1).querySelector('.step-dot').getBoundingClientRect();
    const span=Math.max(1,last.top-first.top);
    const fill=reduced.matches?1:Math.max(0,Math.min(1,(innerHeight*.64-first.top-first.height/2)/span));
    timeline.style.setProperty('--journey-progress',fill);
    timeline.style.setProperty('--journey-line-height',`${span}px`);
    steps.forEach(step=>step.classList.toggle('active',reduced.matches || step.querySelector('.step-dot').getBoundingClientRect().top<innerHeight*.64));
  }
  const updateScroll = () => { scrollFrame=0; const max=document.documentElement.scrollHeight-innerHeight; progress.style.transform=`scaleX(${max>0?scrollY/max:0})`;document.querySelector('.site-header').classList.toggle('is-scrolled',scrollY>40);const statement=document.querySelector('.statement');if(statement){const rect=statement.getBoundingClientRect();statement.style.setProperty('--reading-progress',Math.max(0,Math.min(1,(innerHeight-rect.top)/(innerHeight*.65))));} };
  addEventListener('scroll',()=>{if(!scrollFrame)scrollFrame=requestAnimationFrame(()=>{updateScroll();updateJourney();});},{passive:true});
  addEventListener('resize',updateJourney);reduced.addEventListener('change',updateJourney);document.addEventListener('site-motion',updateJourney);
  document.fonts.ready.then(updateJourney);updateScroll();updateJourney();
  const mobile = matchMedia('(max-width: 1050px)');
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#main-nav');
  const header = document.querySelector('.site-header');
  const dropdowns = [...nav.querySelectorAll('.nav-dropdown')];
  let menuOpen = false;
  let hoverTimer;
  function closeDropdowns(except) {
    dropdowns.forEach(item => { if (item !== except) item.open = false; });
  }
  function setMenu(open, restoreFocus = false) {
    menuOpen = open && mobile.matches;
    toggle.setAttribute('aria-expanded', String(menuOpen));
    toggle.setAttribute('aria-label', menuOpen ? 'Close menu' : 'Open menu');
    toggle.querySelector('.menu-label').textContent = menuOpen ? 'Close' : 'Menu';
    nav.dataset.collapsed = String(mobile.matches && !menuOpen);
    nav.inert = mobile.matches && !menuOpen;
    header.classList.toggle('menu-open', menuOpen);
    if (!menuOpen) closeDropdowns();
    if (restoreFocus) toggle.focus({preventScroll:true});
    positionMenu();
  }
  function positionMenu() {
    header.style.setProperty('--menu-height', `${Math.max(120,innerHeight-header.getBoundingClientRect().bottom-12)}px`);
  }
  function syncMenu() { clearTimeout(hoverTimer); toggle.hidden = !mobile.matches; setMenu(false); }
  header.classList.add('nav-enhanced');
  syncMenu(); mobile.addEventListener('change', syncMenu);
  toggle.addEventListener('click', () => setMenu(!menuOpen));
  dropdowns.forEach(item => {
    const summary = item.querySelector('summary');
    summary.addEventListener('click', () => { clearTimeout(hoverTimer); closeDropdowns(item); });
    item.addEventListener('pointerenter', event => {
      if (mobile.matches || event.pointerType !== 'mouse') return;
      clearTimeout(hoverTimer);
      hoverTimer = setTimeout(() => { closeDropdowns(item); item.open = true; },120);
    });
    item.addEventListener('pointerleave', event => {
      if (mobile.matches || event.pointerType !== 'mouse') return;
      clearTimeout(hoverTimer);
      hoverTimer = setTimeout(() => { if (!item.contains(document.activeElement)) item.open = false; },180);
    });
    summary.addEventListener('keydown', event => {
      if (event.key === 'ArrowDown') {
        event.preventDefault(); closeDropdowns(item); item.open = true;
        item.querySelector('a').focus();
      }
    });
  });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    clearTimeout(hoverTimer);
    const openDropdown = dropdowns.find(item => item.open);
    if (openDropdown) { event.preventDefault(); openDropdown.open = false; openDropdown.querySelector('summary').focus(); }
    else if (menuOpen) { event.preventDefault(); setMenu(false,true); }
  });
  document.addEventListener('click', event => {
    if (!header.contains(event.target)) { clearTimeout(hoverTimer); setMenu(false); }
  });
  header.addEventListener('focusout', event => {
    if (!header.contains(event.relatedTarget)) { clearTimeout(hoverTimer); setMenu(false); }
    else dropdowns.forEach(item => { if (item.contains(event.target) && !item.contains(event.relatedTarget)) item.open = false; });
  });
  nav.addEventListener('click', event => { if (event.target.closest('a')) setMenu(false); });
  addEventListener('resize', positionMenu);
  addEventListener('scroll', positionMenu, {passive:true});
  const filters = document.querySelector('.filters');
  if(filters) {
    filters.hidden = false;
    filters.addEventListener('click', e => {
      const button = e.target.closest('[data-filter]'); if(!button) return;
      filters.querySelectorAll('button').forEach(b => { b.classList.toggle('active', b === button); b.setAttribute('aria-pressed',String(b === button)); });
      let visible = 0;
      document.querySelectorAll('.treatment-directory .treatment-card').forEach(card => { card.hidden = button.dataset.filter !== 'all' && card.dataset.category !== button.dataset.filter; if(!card.hidden) visible++; });
      document.querySelector('.filter-status').textContent = `${visible} treatments shown.`;
    });
  }
  document.querySelectorAll('.imaging-explorer').forEach(explorer=>{
    const views={opg:{src:'imaging-0.webp',alt:'Panoramic dental X-ray example from the practice website',title:'A wider view of your teeth and jaws.',copy:'A panoramic image helps your clinician see the bigger picture.',index:'01 / 02'},cbct:{src:'imaging-1.webp',alt:'Three-dimensional CBCT dental scan example from the practice website',title:'Another dimension in treatment planning.',copy:'A 3D scan can help your clinician assess structures from different perspectives.',index:'02 / 02'}};
    explorer.querySelectorAll('[data-scan]').forEach(button=>button.addEventListener('click',()=>{const v=views[button.dataset.scan];explorer.querySelectorAll('[data-scan]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));const img=explorer.querySelector('[data-scan-image]');img.src='/assets/'+v.src;img.alt=v.alt;explorer.querySelector('[data-scan-title]').textContent=v.title;explorer.querySelector('[data-scan-copy]').textContent=v.copy;explorer.querySelector('.scan-index').textContent=v.index;const screen=explorer.querySelector('.scan-screen');screen.classList.remove('changing');requestAnimationFrame(()=>screen.classList.add('changing'));}));
  });
  const context = document.querySelector('.enquiry-context');
  if(context) {
    const treatment = new URLSearchParams(location.search).get('treatment');
    const labels = {'white-fillings':'white fillings','dental-implants':'dental implants','invisible-braces':'invisible braces','root-canal':'root canal treatment','dental-hygiene':'dental hygiene','wisdom-teeth':'wisdom-tooth care','sedation':'conscious sedation','smile-makeovers':'smile makeovers','teeth-whitening':'teeth whitening','facial-aesthetics':'facial aesthetics','stress-therapy':'stress therapy','microdermabrasion':'microdermabrasion','microneedling':'microneedling','imaging':'dental imaging'};
    if(labels[treatment]) { context.textContent = `Interested in ${labels[treatment]}? Mention this when you contact the team.`; context.hidden = false; }
  }
  if('IntersectionObserver' in window && !reduced.matches) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => { if(entry.isIntersecting) { entry.target.classList.add('fade-enter'); observer.unobserve(entry.target); } }), {threshold:.12});
    document.querySelectorAll('.section-heading,.care-strip .wrap>div,.step-copy,.side-panel,.treatment-card,.team-card,.info-grid article,.image-feature,.location-grid>div,.footer-grid>*,.imaging-explorer').forEach((el,i) => {el.style.setProperty('--reveal-delay',`${(i%3)*90}ms`);observer.observe(el);});
  }
  // Let decorative motion rest offscreen without hiding any content.
  if ('IntersectionObserver' in window) {
    const motionObserver = new IntersectionObserver(entries => entries.forEach(entry => {
      entry.target.classList.toggle('motion-in-view', entry.isIntersecting);
    }));
    document.querySelectorAll('.tooth-art').forEach(el => motionObserver.observe(el));
  }
  if (navigator.connection?.saveData) document.documentElement.classList.add('save-data');
})();
