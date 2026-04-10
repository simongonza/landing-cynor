/* ============================================
   CYNOR - Main JavaScript
   Innovation that thinks in data.
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
  initLoader();
  initNavbar();
  initMobileMenu();
  initScrollReveal();
  initBackToTop();
  initParticles();
  initCounterAnimation();
  initFormValidation();
  initCookieBar();
  initSmoothScroll();
});

/* ---------- Loader ---------- */
function initLoader() {
  const loader = document.querySelector('.loader');
  if (!loader) return;

  window.addEventListener('load', () => {
    setTimeout(() => {
      loader.classList.add('hidden');
      document.body.style.overflow = '';
    }, 800);
  });

  // Fallback: hide after 3s max
  setTimeout(() => {
    loader.classList.add('hidden');
    document.body.style.overflow = '';
  }, 3000);
}

/* ---------- Navbar Scroll Effect ---------- */
function initNavbar() {
  const navbar = document.querySelector('.navbar');
  if (!navbar) return;

  let lastScroll = 0;

  const handleScroll = () => {
    const scrollY = window.scrollY;

    if (scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }

    lastScroll = scrollY;
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();
}

/* ---------- Mobile Menu ---------- */
function initMobileMenu() {
  const hamburger = document.querySelector('.hamburger');
  const mobileMenu = document.querySelector('.mobile-menu');
  if (!hamburger || !mobileMenu) return;

  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    mobileMenu.classList.toggle('active');

    if (mobileMenu.classList.contains('active')) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
  });

  // Close menu when clicking a link
  mobileMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      hamburger.classList.remove('active');
      mobileMenu.classList.remove('active');
      document.body.style.overflow = '';
    });
  });

  // Close on escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && mobileMenu.classList.contains('active')) {
      hamburger.classList.remove('active');
      mobileMenu.classList.remove('active');
      document.body.style.overflow = '';
    }
  });
}

/* ---------- Scroll Reveal Animations ---------- */
function initScrollReveal() {
  const reveals = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale');
  if (!reveals.length) return;

  const observerOptions = {
    root: null,
    rootMargin: '0px 0px -80px 0px',
    threshold: 0.1
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  reveals.forEach(el => observer.observe(el));
}

/* ---------- Back to Top ---------- */
function initBackToTop() {
  const btn = document.querySelector('.back-to-top');
  if (!btn) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 600) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  }, { passive: true });

  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

/* ---------- Particles ---------- */
function initParticles() {
  const container = document.querySelector('.hero__particles');
  if (!container) return;

  const particleCount = 20;

  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement('div');
    particle.classList.add('hero__particle');
    particle.style.left = `${Math.random() * 100}%`;
    particle.style.top = `${Math.random() * 100}%`;
    particle.style.animationDelay = `${Math.random() * 8}s`;
    particle.style.animationDuration = `${6 + Math.random() * 8}s`;

    const size = 2 + Math.random() * 4;
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;

    container.appendChild(particle);
  }
}

/* ---------- Counter Animation ---------- */
function initCounterAnimation() {
  const counters = document.querySelectorAll('.stat__number[data-target]');
  if (!counters.length) return;

  const observerOptions = {
    threshold: 0.5
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  counters.forEach(counter => observer.observe(counter));
}

function animateCounter(element) {
  const target = parseInt(element.dataset.target);
  const suffix = element.dataset.suffix || '';
  const duration = 2000;
  const start = performance.now();

  function update(currentTime) {
    const elapsed = currentTime - start;
    const progress = Math.min(elapsed / duration, 1);

    // Ease out cubic
    const easeProgress = 1 - Math.pow(1 - progress, 3);
    const current = Math.round(easeProgress * target);

    element.textContent = current + suffix;

    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }

  requestAnimationFrame(update);
}

/* ---------- Form Validation ---------- */
function initFormValidation() {
  const form = document.querySelector('#contactForm');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    let isValid = true;
    const fields = form.querySelectorAll('[required]');

    fields.forEach(field => {
      removeError(field);

      if (!field.value.trim()) {
        showError(field, 'Este campo es obligatorio');
        isValid = false;
      } else if (field.type === 'email' && !isValidEmail(field.value)) {
        showError(field, 'Ingresa un email válido');
        isValid = false;
      }
    });

    if (isValid) {
      const btn = form.querySelector('.btn--primary');
      const originalText = btn.textContent;
      btn.textContent = '✓ Mensaje Enviado';
      btn.style.background = 'rgba(212, 225, 87, 0.2)';
      btn.style.color = '#D4E157';
      btn.style.border = '1px solid rgba(212, 225, 87, 0.4)';
      btn.disabled = true;

      setTimeout(() => {
        btn.textContent = originalText;
        btn.style.background = '';
        btn.style.color = '';
        btn.style.border = '';
        btn.disabled = false;
        form.reset();
      }, 3000);
    }
  });
}

function showError(field, message) {
  field.style.borderColor = '#ff6b6b';
  const error = document.createElement('span');
  error.className = 'form-error';
  error.textContent = message;
  error.style.cssText = 'color: #ff6b6b; font-size: 0.8rem; margin-top: 4px; display: block; font-family: "DM Sans", sans-serif;';
  field.parentNode.appendChild(error);
}

function removeError(field) {
  field.style.borderColor = '';
  const error = field.parentNode.querySelector('.form-error');
  if (error) error.remove();
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

/* ---------- Cookie Bar ---------- */
function initCookieBar() {
  const bar = document.querySelector('.notification-bar');
  if (!bar) return;

  const accepted = localStorage.getItem('cynor_cookies_accepted');
  if (!accepted) {
    setTimeout(() => {
      bar.classList.add('visible');
    }, 2000);
  }

  const acceptBtn = bar.querySelector('.btn');
  if (acceptBtn) {
    acceptBtn.addEventListener('click', () => {
      localStorage.setItem('cynor_cookies_accepted', 'true');
      bar.classList.remove('visible');
    });
  }
}

/* ---------- Smooth Scroll ---------- */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href === '#') return;

      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        const offset = 80;
        const top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    });
  });
}

/* ---------- Typing Effect (optional) ---------- */
function initTypingEffect(element, texts, speed = 80, pause = 2000) {
  if (!element) return;

  let textIndex = 0;
  let charIndex = 0;
  let isDeleting = false;

  function type() {
    const currentText = texts[textIndex];

    if (isDeleting) {
      element.textContent = currentText.substring(0, charIndex - 1);
      charIndex--;
    } else {
      element.textContent = currentText.substring(0, charIndex + 1);
      charIndex++;
    }

    let timeout = isDeleting ? speed / 2 : speed;

    if (!isDeleting && charIndex === currentText.length) {
      timeout = pause;
      isDeleting = true;
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      textIndex = (textIndex + 1) % texts.length;
      timeout = 500;
    }

    setTimeout(type, timeout);
  }

  type();
}

/* ---------- Data Deletion Form ---------- */
function initDeletionForm() {
  const form = document.querySelector('#deletionForm');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    let isValid = true;
    const fields = form.querySelectorAll('[required]');

    fields.forEach(field => {
      removeError(field);
      if (!field.value.trim()) {
        showError(field, 'Este campo es obligatorio');
        isValid = false;
      } else if (field.type === 'email' && !isValidEmail(field.value)) {
        showError(field, 'Ingresa un email válido');
        isValid = false;
      }
    });

    const checkbox = form.querySelector('#confirmDeletion');
    if (checkbox && !checkbox.checked) {
      showError(checkbox, 'Debes confirmar esta acción');
      isValid = false;
    }

    if (isValid) {
      const btn = form.querySelector('.btn--primary');
      btn.textContent = '✓ Solicitud Enviada';
      btn.style.background = 'rgba(212, 225, 87, 0.2)';
      btn.style.color = '#D4E157';
      btn.disabled = true;

      setTimeout(() => {
        form.reset();
        btn.textContent = 'Enviar Solicitud';
        btn.style.background = '';
        btn.style.color = '';
        btn.disabled = false;
      }, 4000);
    }
  });
}

// Initialize deletion form if on that page
document.addEventListener('DOMContentLoaded', initDeletionForm);
