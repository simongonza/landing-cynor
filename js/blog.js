// Blog Cynor: los artículos son páginas propias (/blog/<slug>), generadas por scripts/build.py.
(function () {
  // Enlaces viejos (/blog#post-<slug>) siguen funcionando
  var m = window.location.hash.match(/^#post-([\w-]+)$/);
  if (m) { window.location.replace('/blog/' + m[1]); return; }

  // Filtro Todo / Vlog / Artículos
  var bar = document.querySelector('[data-blog-filter]');
  var list = document.getElementById('blog-list');
  if (!bar || !list) return;
  var cards = Array.prototype.slice.call(list.querySelectorAll('[data-tipo]'));
  bar.hidden = false;
  bar.addEventListener('click', function (e) {
    var btn = e.target.closest('button[data-f]');
    if (!btn) return;
    var f = btn.getAttribute('data-f');
    Array.prototype.forEach.call(bar.querySelectorAll('button'), function (b) {
      var on = b === btn;
      b.classList.toggle('is-on', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    list.classList.toggle('is-filtered', f !== 'todo');
    cards.forEach(function (c) { c.hidden = f !== 'todo' && c.getAttribute('data-tipo') !== f; });
  });
})();
