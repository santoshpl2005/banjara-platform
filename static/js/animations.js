/* ============================================================
   BANJARA PLATFORM — ANIMATIONS JAVASCRIPT
   Save as: static/js/animations.js
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

  // 1. SCROLL REVEAL
  const revealEls = document.querySelectorAll('.reveal,.reveal-left,.reveal-right,.reveal-zoom,.stagger-children');
  if (revealEls.length) {
    const obs = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); } });
    }, { threshold: 0.12 });
    revealEls.forEach(el => obs.observe(el));
  }

  // 2. AUTO REVEAL CARDS ON SCROLL
  const selectors = ['.temple-card','.icard','.sati-card','.dbox','.fbox','.summary-item','.song-card','.video-card','.yt-card','.quick-fact','.feature-card','.fcard','.stat-card','.action-btn','.gcard','.pcard'];
  selectors.forEach(sel => {
    document.querySelectorAll(sel).forEach((el, i) => {
      el.style.cssText += `opacity:0;transform:translateY(40px);transition:opacity 0.6s ease ${i*0.08}s,transform 0.6s ease ${i*0.08}s`;
      const o = new IntersectionObserver((entries) => {
        entries.forEach(e => { if (e.isIntersecting) { e.target.style.opacity='1'; e.target.style.transform='translateY(0)'; o.unobserve(e.target); } });
      }, { threshold: 0.1 });
      o.observe(el);
    });
  });

  // 3. COUNTER ANIMATION
  function animateCounter(el) {
    const target = parseInt(el.textContent.replace(/\D/g,'')) || 0;
    if (!target) return;
    let cur = 0;
    const step = Math.max(1, Math.floor(target/40));
    const t = setInterval(() => { cur = Math.min(cur+step,target); el.textContent=cur; if(cur>=target) clearInterval(t); }, 40);
  }
  const cObs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const n = e.target.querySelector('.stat-num,.sm-num,.wn');
        if (n && !n.dataset.animated) { n.dataset.animated='1'; animateCounter(n); }
        cObs.unobserve(e.target);
      }
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('.stat-card,.stat-mini,.wb-stat').forEach(el => cObs.observe(el));

  // 4. BACK TO TOP
  const topBtn = document.createElement('button');
  topBtn.id = 'back-to-top';
  topBtn.innerHTML = '▲';
  document.body.appendChild(topBtn);
  window.addEventListener('scroll', () => { topBtn.classList.toggle('visible', window.scrollY > 300); });
  topBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

  // 5. PROGRESS BAR ANIMATION
  const pObs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const w = e.target.getAttribute('data-width') || e.target.style.width;
        e.target.style.width='0';
        setTimeout(() => { e.target.style.transition='width 1.2s cubic-bezier(.25,.46,.45,.94)'; e.target.style.width=w; }, 200);
        pObs.unobserve(e.target);
      }
    });
  }, { threshold: 0.3 });
  document.querySelectorAll('.progress-fill').forEach(el => {
    el.setAttribute('data-width', el.style.width || '0%');
    pObs.observe(el);
  });

  // 6. RIPPLE ON BUTTONS
  document.querySelectorAll('button,.btn,.tab-btn,.fbtn,.stab').forEach(btn => {
    btn.addEventListener('click', function(e) {
      const r = document.createElement('span');
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width,rect.height);
      r.style.cssText = `position:absolute;border-radius:50%;background:rgba(255,255,255,.25);width:${size}px;height:${size}px;left:${e.clientX-rect.left-size/2}px;top:${e.clientY-rect.top-size/2}px;transform:scale(0);animation:rippleAnim .6s ease-out;pointer-events:none`;
      if(getComputedStyle(this).position==='static') this.style.position='relative';
      this.style.overflow='hidden';
      this.appendChild(r);
      setTimeout(()=>r.remove(), 700);
    });
  });

  // 7. SMOOTH TAB TRANSITIONS
  const origTab = window.showTab;
  if (typeof origTab === 'function') {
    window.showTab = function(name, btn) {
      const cur = document.querySelector('.tab-section.active');
      if (cur) { cur.style.opacity='0'; cur.style.transform='translateY(8px)'; cur.style.transition='all 0.15s ease'; }
      setTimeout(() => {
        origTab(name, btn);
        const next = document.querySelector('.tab-section.active');
        if (next) { next.style.opacity='0'; next.style.transform='translateY(16px)'; next.style.transition='all 0.35s ease'; setTimeout(()=>{ next.style.opacity='1'; next.style.transform='translateY(0)'; },30); }
      }, 120);
    };
  }

  // 8. GALLERY SECTION TRANSITIONS
  const origSec = window.showSection;
  if (typeof origSec === 'function') {
    window.showSection = function(name, tab) {
      const cur = document.querySelector('.gsection.active');
      if (cur) { cur.style.opacity='0'; cur.style.transform='translateX(-16px)'; cur.style.transition='all 0.2s ease'; }
      setTimeout(() => {
        origSec(name, tab);
        const next = document.getElementById('sec-'+name);
        if (next) { next.style.opacity='0'; next.style.transform='translateX(16px)'; next.style.transition='all 0.35s ease'; setTimeout(()=>{ next.style.opacity='1'; next.style.transform='translateX(0)'; },30); }
      }, 160);
    };
  }

  // 9. NAVBAR HIDE ON SCROLL
  let lastY = 0;
  const nav = document.querySelector('nav');
  if (nav) {
    window.addEventListener('scroll', () => {
      const y = window.scrollY;
      nav.style.transition = 'transform 0.3s ease';
      nav.style.transform = (y > lastY && y > 80) ? 'translateY(-100%)' : 'translateY(0)';
      lastY = y;
    });
  }

  // 10. LAZY IMAGE FADE
  document.querySelectorAll('img').forEach(img => {
    img.style.transition='opacity 0.5s ease';
    if (!img.complete) {
      img.style.opacity='0';
      img.addEventListener('load', ()=>{ img.style.opacity='1'; });
      img.addEventListener('error', ()=>{ img.style.opacity='0.3'; });
    }
  });

  // 11. SPARKLE PARTICLES IN HERO
  const hero = document.querySelector('.page-title');
  if (hero) {
    hero.style.position='relative'; hero.style.overflow='hidden';
    setInterval(() => {
      const p = document.createElement('div');
      p.style.cssText=`position:absolute;width:5px;height:5px;background:rgba(255,215,0,${.2+Math.random()*.5});border-radius:50%;left:${Math.random()*100}%;top:${Math.random()*100}%;pointer-events:none;animation:particleFlyAnim ${2+Math.random()*3}s ease-out forwards;z-index:0`;
      hero.appendChild(p);
      setTimeout(()=>p.remove(),5000);
    }, 900);
  }

  // 12. CARD 3D TILT
  document.querySelectorAll('.stat-card,.song-card').forEach(card => {
    card.addEventListener('mousemove', function(e) {
      const r=this.getBoundingClientRect();
      const rx=((e.clientY-r.top-r.height/2)/r.height)*6;
      const ry=((e.clientX-r.left-r.width/2)/r.width)*-6;
      this.style.transform=`perspective(700px) rotateX(${rx}deg) rotateY(${ry}deg) translateY(-5px)`;
      this.style.transition='transform 0.1s ease';
    });
    card.addEventListener('mouseleave', function() {
      this.style.transform='';
      this.style.transition='transform 0.5s ease';
    });
  });

  // 13. INPUT LABEL ANIMATION
  document.querySelectorAll('input,textarea').forEach(inp => {
    inp.addEventListener('focus', function() {
      const lbl=this.previousElementSibling;
      if(lbl&&lbl.tagName==='LABEL') { lbl.style.color='#8B1A1A'; lbl.style.transition='color 0.3s ease'; }
    });
    inp.addEventListener('blur', function() {
      const lbl=this.previousElementSibling;
      if(lbl&&lbl.tagName==='LABEL') lbl.style.color='';
    });
  });

  // 14. PAGE LOAD BAR
  const bar = document.createElement('div');
  bar.style.cssText='position:fixed;top:0;left:0;height:3px;background:linear-gradient(90deg,#8B1A1A,#ffd700);z-index:9999;width:0;transition:width 0.3s ease';
  document.body.appendChild(bar);
  let prog=0;
  const lt = setInterval(()=>{ prog=Math.min(prog+Math.random()*15,90); bar.style.width=prog+'%'; },120);
  window.addEventListener('load',()=>{ clearInterval(lt); bar.style.width='100%'; setTimeout(()=>{ bar.style.opacity='0'; },400); });

  // 15. MINI-BOX STAGGER ON TAB SWITCH
  function staggerMini() {
    document.querySelectorAll('.tab-section.active .mini-box').forEach((b,i)=>{
      b.style.opacity='0'; b.style.transform='scale(0.8)';
      setTimeout(()=>{ b.style.transition='all 0.35s cubic-bezier(.34,1.56,.64,1)'; b.style.opacity='1'; b.style.transform='scale(1)'; },i*55);
    });
  }
  document.querySelectorAll('.tab-btn,.stab').forEach(btn=>btn.addEventListener('click',()=>setTimeout(staggerMini,200)));
  staggerMini();

  // 16. ALERT DISMISS
  document.querySelectorAll('.success,.error').forEach(a => {
    setTimeout(()=>{ a.style.transition='all 1s ease'; a.style.opacity='0'; a.style.maxHeight='0'; a.style.overflow='hidden'; a.style.padding='0'; a.style.margin='0'; }, 5000);
  });

  // 17. TABLE ROW HOVER
  document.querySelectorAll('tbody tr').forEach(r=>{
    r.style.transition='all 0.2s ease';
    r.addEventListener('mouseenter',function(){ this.style.transform='scale(1.004)'; });
    r.addEventListener('mouseleave',function(){ this.style.transform=''; });
  });

  // 18. FLOATING EMOJIS IN BANNERS
  document.querySelectorAll('.sec-hero,.hero-banner,.welcome-banner').forEach(sec=>{
    ['🌿','✦','🙏','⭐'].forEach((em,i)=>{
      const s=document.createElement('span');
      s.textContent=em;
      s.style.cssText=`position:absolute;font-size:${14+Math.random()*14}px;opacity:0.07;pointer-events:none;left:${10+Math.random()*80}%;top:${10+Math.random()*80}%;animation:floatAnim ${3+i}s ease-in-out infinite;animation-delay:${i*.5}s;z-index:0`;
      sec.style.position=sec.style.position||'relative';
      sec.appendChild(s);
    });
  });

  // 19. INJECT KEYFRAMES
  const kf = document.createElement('style');
  kf.textContent=`
    @keyframes rippleAnim { to { transform:scale(4); opacity:0; } }
    @keyframes particleFlyAnim { 0%{transform:translateY(0) scale(1);opacity:1} 100%{transform:translateY(-80px) translateX(15px) scale(0);opacity:0} }
    @keyframes floatAnim { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)} }
  `;
  document.head.appendChild(kf);

  console.log('🌿 Banjara Platform — Animations Active! Jai Sevalal! 🙏');
});