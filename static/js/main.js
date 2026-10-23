// Mobile menu
const toggle = document.getElementById('navToggle');
const menu = document.getElementById('navMenu');
if (toggle && menu) {
  toggle.addEventListener('click', () => {
    menu.classList.toggle('open');
    toggle.classList.toggle('active');
  });
}

// Mobile dropdown tap-to-open
document.querySelectorAll('.nav__droptrig').forEach(trig => {
  trig.addEventListener('click', e => {
    if (window.innerWidth <= 900) {
      e.preventDefault();
      trig.parentElement.classList.toggle('open-drop');
      const dm = trig.nextElementSibling;
      if (dm) dm.style.display = dm.style.display === 'block' ? 'none' : 'block';
    }
  });
});

// Scroll reveal
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
}, { threshold: 0.12 });
document.querySelectorAll('[data-reveal]').forEach(el => io.observe(el));

// Regulatory popup modal: shows on first entry, stays dismissed once accepted
const popup = document.getElementById('popup');
if (popup) {
  const SEEN_KEY = 'strikepoint-disclaimer-accepted';
  const accepted = localStorage.getItem(SEEN_KEY);

  if (!accepted) {
    popup.classList.remove('hide');
    document.body.style.overflow = 'hidden';
  } else {
    popup.classList.add('hide');
  }

  const accept = document.getElementById('popupAccept');
  const dismiss = () => {
    localStorage.setItem(SEEN_KEY, '1');
    popup.classList.add('hide');
    document.body.style.overflow = '';
  };
  if (accept) accept.addEventListener('click', dismiss);
}


document.querySelectorAll('[data-slider]').forEach(slider => {
  const track = slider.querySelector('.csr-track');
  const slides = slider.querySelectorAll('.csr-slide');
  if (slides.length <= 1) return;
  const dotsWrap = slider.querySelector('.csr-dots');
  let i = 0;
  const go = n => {
    i = (n + slides.length) % slides.length;
    track.style.transform = `translateX(-${i * 100}%)`;
    dotsWrap?.querySelectorAll('button').forEach((d, x) => d.classList.toggle('active', x === i));
  };
  if (dotsWrap) slides.forEach((_, x) => {
    const b = document.createElement('button');
    if (x === 0) b.classList.add('active');
    b.addEventListener('click', () => go(x));
    dotsWrap.appendChild(b);
  });
  slider.querySelector('.csr-next')?.addEventListener('click', () => go(i + 1));
  slider.querySelector('.csr-prev')?.addEventListener('click', () => go(i - 1));
});