/* The AI Disciple — site behavior. Progressive enhancement only:
   every piece of content is present in the HTML before this runs. */
(function () {
  'use strict';

  /* ---------- Theme ---------- */
  var root = document.documentElement;
  var toggle = document.querySelector('[data-theme-toggle]');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var current =
        root.getAttribute('data-theme') ||
        (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      var next = current === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      toggle.setAttribute('aria-label', 'Switch to ' + (next === 'dark' ? 'light' : 'dark') + ' mode');
    });
  }

  /* ---------- Mobile nav ---------- */
  var navBtn = document.querySelector('[data-nav-toggle]');
  var nav = document.getElementById('primary-nav');
  if (navBtn && nav) {
    navBtn.addEventListener('click', function () {
      var open = nav.getAttribute('data-open') === 'true';
      nav.setAttribute('data-open', String(!open));
      navBtn.setAttribute('aria-expanded', String(!open));
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.setAttribute('data-open', 'false');
        navBtn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---------- Header scroll state ---------- */
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () {
      header.setAttribute('data-scrolled', String(window.scrollY > 8));
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- Fallback scroll reveal for browsers without animation-timeline ---------- */
  var supportsTimeline = CSS.supports && CSS.supports('animation-timeline', 'view()');
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!supportsTimeline && !reduced && 'IntersectionObserver' in window) {
    var items = document.querySelectorAll('.reveal');
    if (items.length) {
      var io = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.style.transition = 'opacity 0.7s cubic-bezier(0.16,1,0.3,1)';
              entry.target.style.opacity = '1';
              io.unobserve(entry.target);
            }
          });
        },
        { rootMargin: '0px 0px -8% 0px', threshold: 0.05 }
      );
      items.forEach(function (el) {
        el.style.opacity = '0';
        io.observe(el);
      });
    }
  }

  /* ---------- Contact form (AJAX, keeps people on the page) ---------- */
  document.querySelectorAll('form[data-ajax-form]').forEach(function (form) {
    var status = form.querySelector('.form__status');
    var submit = form.querySelector('button[type="submit"]');
    form.addEventListener('submit', function (e) {
      if (!form.action || form.action.indexOf('formspree') === -1) return;
      e.preventDefault();
      if (form.querySelector('.hp input') && form.querySelector('.hp input').value) return;
      var label = submit ? submit.textContent : '';
      if (submit) {
        submit.disabled = true;
        submit.textContent = 'Sending…';
      }
      if (status) {
        status.textContent = '';
        status.removeAttribute('data-state');
      }
      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      })
        .then(function (res) {
          if (!res.ok) throw new Error('bad response');
          form.reset();
          if (status) {
            status.textContent =
              'Thank you — your message is in. I reply within one business day.';
            status.setAttribute('data-state', 'ok');
          }
        })
        .catch(function () {
          if (status) {
            status.textContent =
              'Something went wrong. Please email info@theaidisciple.com directly and I will get straight back to you.';
            status.setAttribute('data-state', 'err');
          }
        })
        .finally(function () {
          if (submit) {
            submit.disabled = false;
            submit.textContent = label;
          }
        });
    });
  });

  /* ---------- Library filter (filters DOM already rendered server-side) ---------- */
  function initLibrary(cfg) {
    var grid = document.getElementById(cfg.grid);
    if (!grid) return;
    var items = Array.prototype.slice.call(grid.querySelectorAll('.story'));
    var input = document.getElementById(cfg.search);
    var meta = document.getElementById(cfg.meta);
    var empty = document.getElementById(cfg.empty);
    var chips = Array.prototype.slice.call(document.querySelectorAll('[' + cfg.attr + ']'));
    var facet = 'all';
    var term = '';
    var total = items.length;

    function apply() {
      var shown = 0;
      items.forEach(function (el) {
        var okFacet = facet === 'all' || el.getAttribute(cfg.data) === facet;
        var okTerm = !term || (el.getAttribute('data-search') || '').indexOf(term) !== -1;
        var visible = okFacet && okTerm;
        el.hidden = !visible;
        if (visible) shown++;
      });
      if (meta) {
        meta.textContent =
          shown === total
            ? 'Showing all ' + total + ' ' + cfg.noun
            : 'Showing ' + shown + ' of ' + total + ' ' + cfg.noun;
      }
      if (empty) empty.hidden = shown !== 0;
    }

    function select(value, focusChip) {
      var match = chips.filter(function (c) {
        return c.getAttribute(cfg.attr) === value;
      })[0];
      if (!match) return false;
      facet = value;
      chips.forEach(function (c) {
        c.setAttribute('aria-pressed', String(c === match));
      });
      if (focusChip && typeof match.scrollIntoView === 'function') {
        match.scrollIntoView({ block: 'nearest', inline: 'center' });
      }
      apply();
      return true;
    }

    if (input) {
      var t;
      input.addEventListener('input', function () {
        clearTimeout(t);
        t = setTimeout(function () {
          term = input.value.trim().toLowerCase();
          apply();
        }, 140);
      });
    }
    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        select(chip.getAttribute(cfg.attr), false);
      });
    });

    /* Deep link: /videos.html?category=guide or /videos.html#guide */
    if (cfg.param) {
      var wanted = '';
      try {
        wanted = new URLSearchParams(window.location.search).get(cfg.param) || '';
      } catch (err) {
        wanted = '';
      }
      if (!wanted && window.location.hash.length > 1) {
        wanted = decodeURIComponent(window.location.hash.slice(1));
      }
      if (wanted) select(wanted, true);
    }

    /* Click-to-load YouTube: keeps the page fast, no iframes until asked */
    grid.addEventListener('click', function (e) {
      var link = e.target.closest('.story__link');
      if (!link) return;
      var id = link.getAttribute('data-video');
      if (!id) return;
      e.preventDefault();
      var thumb = link.querySelector('.story__thumb');
      if (!thumb || thumb.getAttribute('data-loaded') === 'true') return;
      thumb.setAttribute('data-loaded', 'true');
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0';
      f.title = link.getAttribute('data-title') || 'Video';
      f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; picture-in-picture';
      f.allowFullscreen = true;
      f.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;border:0;';
      thumb.appendChild(f);
    });
  }

  initLibrary({
    grid: 'story-grid', search: 'story-search', meta: 'story-meta', empty: 'story-empty',
    attr: 'data-lang-filter', data: 'data-lang', noun: 'stories', param: ''
  });
  initLibrary({
    grid: 'video-grid', search: 'video-search', meta: 'video-meta', empty: 'video-empty',
    attr: 'data-cat-filter', data: 'data-cat', noun: 'videos', param: 'category'
  });

  /* ---------- Lazy-load homepage videos on click ---------- */
  document.querySelectorAll('[data-video-embed]').forEach(function (holder) {
    holder.addEventListener(
      'click',
      function () {
        if (holder.getAttribute('data-loaded') === 'true') return;
        holder.setAttribute('data-loaded', 'true');
        var f = document.createElement('iframe');
        f.src =
          'https://www.youtube-nocookie.com/embed/' +
          holder.getAttribute('data-video-embed') +
          '?autoplay=1&rel=0';
        f.title = holder.getAttribute('data-title') || 'Video';
        f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; picture-in-picture';
        f.allowFullscreen = true;
        holder.appendChild(f);
      },
      { once: true }
    );
  });

  /* ---------- Preselect the contact form topic from ?interest= ---------- */
  (function () {
    var select = document.getElementById('interest');
    if (!select) return;
    var key = new URLSearchParams(window.location.search).get('interest');
    if (!key) return;
    var match = select.querySelector('option[data-key="' + key.replace(/"/g, '') + '"]');
    if (!match) return;
    select.value = match.value;
    var notes = {
      training:
        'Great \u2014 send this and I\u2019ll email you a private link to the free AI training myself, usually within one business day.',
      'church-video':
        'Tell me the passage or the message you have coming up, and roughly when you need it.',
      church:
        'Tell me a little about your church and what you are hoping AI could take off someone\u2019s plate.'
    };
    if (!notes[key]) return;
    var note = document.createElement('p');
    note.className = 'form-fine';
    note.setAttribute('role', 'status');
    note.style.marginTop = 'var(--space-3)';
    note.textContent = notes[key];
    select.parentNode.appendChild(note);
  })();

  /* ---------- Current year ---------- */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
