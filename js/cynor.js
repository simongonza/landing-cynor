/* Cynor - interacciones del sitio. Sin dependencias. */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var WA = '573128861517';

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function track(event, data) {
    window.dataLayer = window.dataLayer || [];
    var payload = { event: event };
    for (var k in data) payload[k] = data[k];
    window.dataLayer.push(payload);
  }
  function waLink(text) { return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(text); }
  function onInView(els, cb, opts) {
    if (!('IntersectionObserver' in window)) { els.forEach(function (el) { cb(el); }); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { cb(e.target); io.unobserve(e.target); }
      });
    }, opts || { threshold: 0.18, rootMargin: '0px 0px -6% 0px' });
    els.forEach(function (el) { io.observe(el); });
  }

  /* Navegación */
  var page = document.body.getAttribute('data-page');
  $$('.nav__links a').forEach(function (a) {
    if (a.getAttribute('data-nav') === page) a.setAttribute('aria-current', 'page');
  });

  var nav = $('#nav');
  if (nav && 'IntersectionObserver' in window) {
    var sentinel = document.createElement('div');
    sentinel.style.cssText = 'position:absolute;top:0;left:0;height:8px;width:1px;pointer-events:none';
    document.body.prepend(sentinel);
    new IntersectionObserver(function (entries) {
      nav.classList.toggle('is-scrolled', !entries[0].isIntersecting);
    }).observe(sentinel);
  }

  var toggle = $('#navToggle');
  var menu = $('#mobileMenu');
  function setMenu(open) {
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
    menu.hidden = !open;
    document.body.style.overflow = open ? 'hidden' : '';
  }
  if (toggle && menu) {
    toggle.addEventListener('click', function () { setMenu(menu.hidden); });
    $$('a', menu).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !menu.hidden) setMenu(false); });
  }

  /* Aparición al hacer scroll */
  onInView($$('[data-reveal]'), function (el) { el.classList.add('is-in'); });
  onInView($$('[data-inview]'), function (el) { el.classList.add('is-in'); }, { threshold: 0.35 });

  /* Palabra rotativa del hero */
  $$('[data-rotator]').forEach(function (rot) {
    var words = $$('.rotator__word', rot);
    if (words.length < 2) return;
    var i = 0;
    function measure() {
      var w = words[i];
      var clone = w.cloneNode(true);
      clone.style.cssText = 'position:absolute;visibility:hidden;transform:none';
      rot.appendChild(clone);
      rot.style.width = clone.getBoundingClientRect().width + 'px';
      rot.removeChild(clone);
    }
    document.fonts && document.fonts.ready.then(measure);
    measure();
    window.addEventListener('resize', measure);
    if (reduceMotion) return;
    setInterval(function () {
      var cur = words[i];
      i = (i + 1) % words.length;
      var next = words[i];
      cur.classList.remove('is-active');
      cur.classList.add('is-leaving');
      next.classList.remove('is-leaving');
      next.classList.add('is-active');
      measure();
      setTimeout(function () { cur.classList.remove('is-leaving'); }, 700);
    }, 2300);
  });

  /* Profundidad con el puntero sobre el sello */
  if (finePointer && !reduceMotion) {
    $$('[data-parallax]').forEach(function (zone) {
      var frame = null;
      zone.addEventListener('pointermove', function (e) {
        if (frame) return;
        frame = requestAnimationFrame(function () {
          var r = zone.getBoundingClientRect();
          zone.style.setProperty('--mx', ((e.clientX - r.left) / r.width - 0.5).toFixed(3));
          zone.style.setProperty('--my', ((e.clientY - r.top) / r.height - 0.5).toFixed(3));
          frame = null;
        });
      });
      zone.addEventListener('pointerleave', function () {
        zone.style.setProperty('--mx', 0);
        zone.style.setProperty('--my', 0);
      });
    });

    $$('[data-tilt]').forEach(function (card) {
      var frame = null;
      card.addEventListener('pointermove', function (e) {
        if (frame) return;
        frame = requestAnimationFrame(function () {
          var r = card.getBoundingClientRect();
          var x = (e.clientX - r.left) / r.width - 0.5;
          var y = (e.clientY - r.top) / r.height - 0.5;
          card.style.setProperty('--ry', (x * 5).toFixed(2) + 'deg');
          card.style.setProperty('--rx', (y * -5).toFixed(2) + 'deg');
          frame = null;
        });
      });
      card.addEventListener('pointerleave', function () {
        card.style.setProperty('--ry', '0deg');
        card.style.setProperty('--rx', '0deg');
      });
    });
  }

  /* Manifiesto: las palabras se encienden en secuencia */
  $$('[data-words]').forEach(function (el) {
    if (reduceMotion) return;
    var html = el.innerHTML;
    var out = html.replace(/(<[^>]+>)|([^<\s]+)/g, function (m, tag, word) {
      return tag ? tag : '<span class="w">' + word + '</span>';
    });
    el.innerHTML = out;
    var words = $$('.w', el);
    words.forEach(function (w) { w.style.setProperty('--o', '.18'); });
    onInView([el], function () {
      words.forEach(function (w, idx) {
        setTimeout(function () { w.style.setProperty('--o', '1'); }, idx * 45);
      });
    }, { threshold: 0.4 });
  });

  /* Dolores: interruptor Sin Cynor / Con Cynor */
  $$('[data-flip]').forEach(function (panel) {
    var btn = $('.switch__btn', panel);
    var touched = false;
    function set(on) {
      panel.classList.toggle('is-on', on);
      btn.setAttribute('aria-checked', String(on));
    }
    btn.addEventListener('click', function () {
      touched = true;
      set(!panel.classList.contains('is-on'));
      track('interruptor_con_cynor', { estado: panel.classList.contains('is-on') ? 'con' : 'sin' });
    });
    $$('.switch__label', panel).forEach(function (label) {
      label.addEventListener('click', function () {
        touched = true;
        set(label.getAttribute('data-side') === 'on');
      });
    });
    // Demostración: si nadie lo ha tocado, se activa solo una vez al verlo
    if (!reduceMotion) {
      onInView([panel], function () {
        setTimeout(function () { if (!touched) set(true); }, 1600);
      }, { threshold: 0.55 });
    }
  });

  /* Tarjetas apiladas: la de abajo se encoge cuando la siguiente la cubre */
  $$('.stack').forEach(function (stack) {
    var cards = $$('.line-card', stack);
    if (cards.length < 2 || !('IntersectionObserver' in window)) return;
    cards.slice(1).forEach(function (card, idx) {
      var prev = cards[idx];
      var io = new IntersectionObserver(function (entries) {
        var e = entries[0];
        var stuckLine = prev.getBoundingClientRect().top + 60;
        prev.classList.toggle('is-under', e.boundingClientRect.top <= stuckLine && e.isIntersecting);
      }, { threshold: [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1] });
      io.observe(card);
    });
  });

  /* Línea de tiempo: avanza a medida que aparecen los momentos */
  $$('[data-timeline]').forEach(function (tl) {
    var moments = $$('.moment', tl);
    var seen = 0;
    onInView(moments, function (m) {
      m.classList.add('is-in');
      seen += 1;
      tl.style.setProperty('--progress', (seen / moments.length).toFixed(3));
    }, { threshold: 0.6 });
  });

  /* Testimonios: flechas */
  $$('[data-quotes]').forEach(function (wrap) {
    var track_ = $('.quotes', wrap);
    $$('[data-dir]', wrap).forEach(function (btn) {
      btn.addEventListener('click', function () {
        var card = $('.quote', track_);
        var step = card ? card.getBoundingClientRect().width + 20 : 400;
        track_.scrollBy({ left: step * Number(btn.getAttribute('data-dir')), behavior: reduceMotion ? 'auto' : 'smooth' });
      });
    });
  });

  /* Calculadora de pacientes y clientes perdidos */
  var money = new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 });
  $$('[data-calc]').forEach(function (calc) {
    var inMsgs = $('[name="msgs"]', calc);
    var inLate = $('[name="late"]', calc);
    var inValue = $('[name="value"]', calc);
    var outMonth = $('[data-out="month"]', calc);
    var outPeople = $('[data-out="people"]', calc);
    var outYear = $('[data-out="year"]', calc);
    var LOST_RATE = 0.3;
    var DAYS = 26;
    var shown = { month: 0, people: 0, year: 0 };
    var used = false;

    function paint(range) {
      var p = (range.value - range.min) / (range.max - range.min) * 100;
      range.style.setProperty('--p', p + '%');
    }
    function tween(key, to, fmt, el) {
      var from = shown[key];
      shown[key] = to;
      if (reduceMotion) { el.textContent = fmt(to); return; }
      var start = performance.now();
      function tick(now) {
        var t = Math.min(1, (now - start) / 550);
        var eased = 1 - Math.pow(1 - t, 3);
        el.textContent = fmt(Math.round(from + (to - from) * eased));
        if (t < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    }
    function update() {
      [inMsgs, inLate, inValue].forEach(paint);
      $('[data-for="msgs"]', calc).textContent = inMsgs.value + ' al día';
      $('[data-for="late"]', calc).textContent = inLate.value + '%';
      $('[data-for="value"]', calc).textContent = money.format(Number(inValue.value));
      var people = Math.round(Number(inMsgs.value) * DAYS * (Number(inLate.value) / 100) * LOST_RATE);
      var month = people * Number(inValue.value);
      tween('month', month, function (n) { return money.format(n); }, outMonth);
      tween('people', people, function (n) { return String(n); }, outPeople);
      tween('year', month * 12, function (n) { return money.format(n); }, outYear);
    }
    [inMsgs, inLate, inValue].forEach(function (r) {
      r.addEventListener('input', function () {
        update();
        if (!used) { used = true; track('calculadora_usada', { pagina: page }); }
      });
    });
    onInView([calc], update, { threshold: 0.25 });
    [inMsgs, inLate, inValue].forEach(paint);
  });

  /* Diagnóstico de 4 preguntas */
  var QUESTIONS = [
    { id: 'negocio', title: '¿Qué tipo de negocio tienes?', options: [
      { v: 'salud', label: 'Consultorio, clínica o centro de salud', icon: 'ph-first-aid-kit' },
      { v: 'servicios', label: 'Empresa de servicios', icon: 'ph-briefcase' },
      { v: 'comercio', label: 'Comercio, tienda o venta online', icon: 'ph-storefront' },
      { v: 'otro', label: 'Otro tipo de negocio', icon: 'ph-dots-three-circle' }
    ] },
    { id: 'dolor', title: '¿Qué es lo que más te frena hoy?', options: [
      { v: 'mensajes', label: 'No alcanzo a responder los mensajes a tiempo', icon: 'ph-chat-circle-dots' },
      { v: 'manual', label: 'Pierdo horas cotizando, cobrando o haciendo seguimiento a mano', icon: 'ph-hourglass-medium' },
      { v: 'clientes', label: 'Me faltan clientes nuevos', icon: 'ph-users-three' },
      { v: 'web', label: 'Tengo visitas, pero no se convierten en ventas', icon: 'ph-cursor-click' }
    ] },
    { id: 'volumen', title: '¿Cuántos mensajes o solicitudes recibes al día?', options: [
      { v: 'bajo', label: 'Menos de 10', icon: 'ph-chat' },
      { v: 'medio', label: 'Entre 10 y 30', icon: 'ph-chats' },
      { v: 'alto', label: 'Entre 30 y 80', icon: 'ph-chats-circle' },
      { v: 'muy-alto', label: 'Más de 80', icon: 'ph-fire' }
    ] },
    { id: 'tiempo', title: '¿Qué tan pronto quieres resolverlo?', options: [
      { v: 'ya', label: 'Este mes', icon: 'ph-lightning' },
      { v: 'pronto', label: 'En 1 a 3 meses', icon: 'ph-calendar-blank' },
      { v: 'explorando', label: 'Solo estoy explorando', icon: 'ph-compass' }
    ] }
  ];

  function recommend(a) {
    if (a.dolor === 'mensajes' && a.negocio === 'salud') return {
      line: 'Agentes IA para salud', href: '/salud',
      title: 'Un agente que atienda y agende por ti',
      steps: ['Responde a tus pacientes por WhatsApp en segundos, a cualquier hora.', 'Agenda, confirma y recuerda las citas sin que tengas que estar pendiente.', 'Te avisa solo cuando una conversación necesita a una persona.']
    };
    if (a.dolor === 'mensajes') return {
      line: 'Agente IA de atención', href: '/automatizaciones',
      title: 'Un agente que responda y filtre por ti',
      steps: ['Responde las preguntas frecuentes de tus clientes al instante.', 'Filtra quién está listo para comprar y te lo pasa con el contexto.', 'Hace seguimiento a quien no respondió, sin que se te olvide.']
    };
    if (a.dolor === 'manual') return {
      line: 'Automatizaciones', href: '/automatizaciones',
      title: 'Que el trabajo repetitivo pase solo',
      steps: ['Mapeamos las tareas que hoy te quitan más horas.', 'Automatizamos la primera (cotizaciones, cobros o seguimientos).', 'Medimos cuánto tiempo recuperas y seguimos con la siguiente.']
    };
    if (a.dolor === 'clientes') return {
      line: 'Pauta digital', href: '/marketing',
      title: 'Campañas que traen clientes, no likes',
      steps: ['Definimos a quién le hablas y cuánto vale un cliente para ti.', 'Lanzamos campañas en Meta y Google con un objetivo claro.', 'Conectamos cada lead a WhatsApp para que no se enfríe.']
    };
    return {
      line: 'Páginas web que convierten', href: '/marketing',
      title: 'Una página que lleve a la acción',
      steps: ['Revisamos dónde se te van los visitantes hoy.', 'Rediseñamos la página con un solo objetivo: que te escriban.', 'Medimos cada clic para seguir mejorando.']
    };
  }

  $$('[data-diag]').forEach(function (root) {
    var stage = $('.diag__stage', root);
    var bars = $$('.diag__steps span', root);
    var count = $('.diag__count', root);
    var answers = {};
    var labels = {};
    var current = 0;
    var preset = root.getAttribute('data-preset') || (page === 'salud' ? 'salud' : null);

    function renderQuestion(idx, back) {
      current = idx;
      var q = QUESTIONS[idx];
      var html = '<div class="q is-entering" role="group" aria-labelledby="q-' + q.id + '">' +
        '<p class="q__title" id="q-' + q.id + '">' + q.title + '</p>';
      q.options.forEach(function (o) {
        var picked = answers[q.id] === o.v ? ' is-picked' : '';
        html += '<button type="button" class="opt' + picked + '" data-v="' + o.v + '"><i class="ph ' + o.icon + '" aria-hidden="true"></i><span>' + o.label + '</span></button>';
      });
      if (idx > 0) html += '<button type="button" class="q__back" data-back><i class="ph ph-arrow-left" aria-hidden="true"></i> Volver</button>';
      html += '</div>';
      stage.innerHTML = html;
      bars.forEach(function (b, i) { b.classList.toggle('is-done', i < idx); });
      count.textContent = 'Pregunta ' + (idx + 1) + ' de ' + QUESTIONS.length;
      if (back !== undefined) { var first = $('.opt', stage); if (first) first.focus({ preventScroll: true }); }
    }

    function renderResult() {
      var r = recommend(answers);
      bars.forEach(function (b) { b.classList.add('is-done'); });
      count.textContent = 'Listo. Este es tu diagnóstico.';
      var msg = 'Hola Cynor, hice el diagnóstico en la web:\n' +
        '• Negocio: ' + labels.negocio + '\n' +
        '• Lo que me frena: ' + labels.dolor + '\n' +
        '• Volumen: ' + labels.volumen + ' al día\n' +
        '• Quiero resolverlo: ' + labels.tiempo.toLowerCase() + '\n' +
        'Me recomendó: ' + r.line + '. ¿Agendamos los 30 minutos?';
      var extra = (answers.volumen === 'alto' || answers.volumen === 'muy-alto') && answers.dolor === 'mensajes'
        ? '<li><i class="ph-fill ph-lightning" aria-hidden="true"></i><span>Con ese volumen de mensajes, cada hora sin responder te cuesta clientes. Es el mejor caso para empezar.</span></li>' : '';
      stage.innerHTML = '<div class="result q is-entering" aria-live="polite">' +
        '<span class="result__line">Te recomendamos: ' + r.line + '</span>' +
        '<h3>' + r.title + '</h3>' +
        '<ul>' + r.steps.map(function (s) { return '<li><i class="ph-fill ph-check-circle" aria-hidden="true"></i><span>' + s + '</span></li>'; }).join('') + extra + '</ul>' +
        '<p class="muted" style="color:#B8B4AA">Lo revisamos contigo en una llamada de 30 minutos, sin costo y sin compromiso.</p>' +
        '<div class="btn-row">' +
        '<a class="btn btn--lime" href="' + waLink(msg) + '" target="_blank" rel="noopener" data-diag-send>Enviar por WhatsApp <i class="ph ph-whatsapp-logo" aria-hidden="true"></i></a>' +
        '<a class="btn btn--ghost" href="' + r.href + '">Ver más</a>' +
        '</div>' +
        '<button type="button" class="q__back" data-restart><i class="ph ph-arrow-counter-clockwise" aria-hidden="true"></i> Volver a empezar</button>' +
        '</div>';
      track('diagnostico_completado', { linea: r.line, negocio: answers.negocio, dolor: answers.dolor, volumen: answers.volumen, tiempo: answers.tiempo });
    }

    stage.addEventListener('click', function (e) {
      var opt = e.target.closest('.opt');
      if (opt) {
        var q = QUESTIONS[current];
        answers[q.id] = opt.getAttribute('data-v');
        labels[q.id] = opt.textContent.trim();
        $$('.opt', stage).forEach(function (b) { b.classList.toggle('is-picked', b === opt); });
        if (current === 0) track('diagnostico_iniciado', { pagina: page });
        setTimeout(function () {
          if (current < QUESTIONS.length - 1) renderQuestion(current + 1, false);
          else renderResult();
        }, reduceMotion ? 0 : 260);
        return;
      }
      if (e.target.closest('[data-back]')) { renderQuestion(current - 1, true); return; }
      if (e.target.closest('[data-restart]')) { answers = {}; labels = {}; renderQuestion(0, true); return; }
      if (e.target.closest('[data-diag-send]')) track('diagnostico_whatsapp', { pagina: page });
    });

    if (preset) {
      var q0 = QUESTIONS[0];
      var o = q0.options.filter(function (x) { return x.v === preset; })[0];
      if (o) { answers.negocio = o.v; labels.negocio = o.label; }
    }
    renderQuestion(preset && answers.negocio ? 1 : 0);
  });

  /* Formulario de contacto */
  var form = $('#contactForm');
  if (form) {
    form.addEventListener('submit', function (e) {
      var ok = true;
      $$('[required]', form).forEach(function (input) {
        var field = input.closest('.field');
        var valid = input.value.trim() !== '' && (input.type !== 'email' || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value.trim()));
        field.classList.toggle('is-invalid', !valid);
        input.setAttribute('aria-invalid', String(!valid));
        if (!valid && ok) { input.focus(); ok = false; }
      });
      if (!ok) { e.preventDefault(); return; }
      track('formulario_contacto', { asunto: form.subject.value });
    });
    $$('input, select, textarea', form).forEach(function (input) {
      input.addEventListener('input', function () {
        var field = input.closest('.field');
        if (field && field.classList.contains('is-invalid') && input.value.trim() !== '') {
          field.classList.remove('is-invalid');
          input.setAttribute('aria-invalid', 'false');
        }
      });
    });
    if (/[?&]enviado=1/.test(location.search)) {
      var status = $('#formStatus');
      if (status) status.hidden = false;
    }
  }

  /* Clics de conversión */
  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-track]');
    if (el) track('clic_' + el.getAttribute('data-track'), { pagina: page });
  });

  /* Cookies */
  var bar = $('#cookieBar');
  if (bar) {
    var accepted = false;
    try { accepted = localStorage.getItem('cynor-cookies') === '1'; } catch (err) { accepted = false; }
    if (!accepted) setTimeout(function () { bar.hidden = false; }, 1500);
    $('#cookieOk').addEventListener('click', function () {
      bar.hidden = true;
      try { localStorage.setItem('cynor-cookies', '1'); } catch (err) { /* sin almacenamiento */ }
    });
  }

  $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
