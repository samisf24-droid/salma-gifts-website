// هدايا سلمى — سكربت صغير:
// 1) فتح القائمة على الموبايل.  2) معاينة الأسماء على الصينية بالرئيسية.
// كل محتوى الموقع مكتوب بالـHTML؛ إذا ما اشتغل السكربت، الزر بيفتح إنستغرام عادي.
(function () {
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('mobile-nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // قياس الضغط على أزرار الحجز (Google Analytics) — كل زر إله اسم بـ data-event
  document.addEventListener('click', function (e) {
    var el = e.target.closest && e.target.closest('[data-event]');
    if (el && typeof window.clarity === 'function') {
      window.clarity('event', 'book_click_' + el.getAttribute('data-event'));
    }
    if (el && typeof window.gtag === 'function') {
      window.gtag('event', 'book_click', { button: el.getAttribute('data-event'), page: location.pathname });
    }
  });

  var toastEl = document.querySelector('.toast');
  var toastTimer;
  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove('show'); }, 6000);
  }

  // تكبير صور المنتجات (الناس كانت تكبس عالصور وما يصير إشي — Clarity: dead clicks)
  var zoomImgs = document.querySelectorAll('.mosaic img, figure.photo img');
  if (zoomImgs.length) {
    var box = document.createElement('div');
    box.className = 'zoom';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-label', 'صورة مكبّرة، اكبسوا للإغلاق');
    box.innerHTML = '<img alt=""><button type="button" aria-label="إغلاق">×</button>';
    document.body.appendChild(box);
    var bigImg = box.querySelector('img');
    var close = function () { box.classList.remove('open'); document.body.style.overflow = ''; };
    box.addEventListener('click', close);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    zoomImgs.forEach(function (im) {
      im.style.cursor = 'zoom-in';
      im.addEventListener('click', function (e) {
        if (im.closest('a')) return;
        e.preventDefault();
        bigImg.src = im.currentSrc || im.src; bigImg.alt = im.alt;
        box.classList.add('open'); document.body.style.overflow = 'hidden';
        if (typeof window.clarity === 'function') window.clarity('event', 'photo_zoom');
      });
    });
  }

  // كاروسيل الموديلات: أزرار سابق/تالي + نسخ اسم الموديل قبل فتح إنستغرام
  document.querySelectorAll('[data-carousel]').forEach(function (car) {
    var track = car.querySelector('.mtrack');
    var step = function (dir) {
      var slide = track.querySelector('.mslide');
      var w = slide ? slide.getBoundingClientRect().width + 14 : 300;
      track.scrollBy({ left: dir * w, behavior: 'smooth' });
    };
    var prev = car.querySelector('.prev'), next = car.querySelector('.next');
    // RTL: السابق = يمين = scrollBy موجب
    if (prev) prev.addEventListener('click', function () { step(1); });
    if (next) next.addEventListener('click', function () { step(-1); });
  });
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-model]');
    if (!b) return;
    var n = b.getAttribute('data-n');
    var msg = 'مرحبًا، أودّ حجز مسكة عروس ' + (n ? 'موديل رقم ' + n + ' ' : 'موديل ') + '«' + b.getAttribute('data-model') + '» (18 دينار)\nمن موقع salmagifts.com';
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(msg).then(function () { toast('نسخنا رقم الموديل. الصقيه في رسالة إنستغرام.'); }, function () {});
      }
    } catch (err) {}
  });

  var form = document.getElementById('maker');
  if (!form) return;

  // ===== تمديد الأسماء بالكشيدة (نفس قاعدة شهادات القِران) =====
  var CONNECT_AFTER = 'بتثجحخسشصضطظعغفقكلمنهيئ';
  function isArabicLetter(c) { return c >= 'آ' && c <= 'ي'; }
  function stretchWord(w, n) {
    w = w.replace(/ـ/g, '');
    var letters = w.replace(/[ً-ْ]/g, '');
    if (letters.length < 2 || n === 0) return w;
    for (var i = w.length - 2; i >= 0; i--) {
      if (CONNECT_AFTER.indexOf(w[i]) > -1 && isArabicLetter(w[i + 1])) {
        return w.slice(0, i + 1) + new Array(n + 1).join('ـ') + w.slice(i + 1);
      }
    }
    return w;
  }
  function target(w) { return w.replace(/[ً-ْـ]/g, '').length >= 4 ? 4 : 3; }
  function stretch(name, n) {
    return name.trim().split(/\s+/).map(function (w) { return stretchWord(w, n === undefined ? target(w) : Math.min(n, target(w))); }).join(' ');
  }

  var stage = form.querySelector('.stage');
  var outs = function (k) { return form.querySelectorAll('[data-out="' + k + '"]'); };
  var groomIn = form.elements.groom, brideIn = form.elements.bride, dateIn = form.elements.date;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function val(input) { return (input.value || '').replace(/\s+/g, ' ').trim() || input.placeholder; }
  function setAll(k, text) { outs(k).forEach(function (el) { el.textContent = text; }); }

  // الاسم الطويل يصغر لحتى يضل جوّا الصينية
  function fitIn(box) {
    var names = box.querySelector('.names');
    if (!names) return;
    names.style.fontSize = '';
    var max = box.clientWidth * 0.8, w = 0;
    names.querySelectorAll('[data-out]').forEach(function (s) { w = Math.max(w, s.scrollWidth); });
    if (w > max) names.style.fontSize = (parseFloat(getComputedStyle(names).fontSize) * max / w) + 'px';
  }
  function fit() { fitIn(form.querySelector('.mirror')); fitIn(form.querySelector('.tag')); }

  var anim;
  function render(which) {
    var g = val(groomIn), b = val(brideIn);
    setAll('gi', g.charAt(0)); setAll('bi', b.charAt(0));
    // التوقيع الحركي: الكشيدة تكبر داخل الاسم وهو ينكتب، وبعدين لمعة تمرّ على المرآة
    cancelAnimationFrame(anim);
    if (reduce) { setAll('g', stretch(g)); setAll('b', stretch(b)); fit(); return; }
    var step = 0, start = null;
    function frame(t) {
      if (start === null) start = t;
      var n = Math.min(4, Math.floor((t - start) / 80));
      if (n !== step || n === 0) {
        step = n;
        setAll('g', stretch(g, n));
        setAll('b', stretch(b, n));
        fit();
      }
      if (n < 4) anim = requestAnimationFrame(frame);
      else shine();
    }
    anim = requestAnimationFrame(frame);
  }
  var shineTimer;
  function shine() {
    clearTimeout(shineTimer);
    shineTimer = setTimeout(function () {
      stage.classList.remove('shine'); void stage.offsetWidth; stage.classList.add('shine');
    }, 250);
  }

  // الكبس على الصينية بيفتح خانة الاسم (بدل ما تكون كبسة ميتة)
  stage.addEventListener('click', function (e) {
    if (e.target.closest && e.target.closest('a')) return;
    var target = !groomIn.value ? groomIn : (!brideIn.value ? brideIn : groomIn);
    target.focus();
  });
  var typing;
  groomIn.addEventListener('input', function () { clearTimeout(typing); typing = setTimeout(function () { render('g'); }, 120); });
  brideIn.addEventListener('input', function () { clearTimeout(typing); typing = setTimeout(function () { render('b'); }, 120); });
  function cleanDate(v) {
    // نقبل 5/3/2027 أو 5-3-2027 أو ٥/٣/٢٠٢٧ ونكتبها مثل الصينية: 05.03.2027
    v = (v || '').replace(/[٠-٩]/g, function (d) { return '٠١٢٣٤٥٦٧٨٩'.indexOf(d); }).trim();
    var m = v.match(/^(\d{1,2})\D+(\d{1,2})\D+(\d{2,4})$/);
    if (!m) return v;
    var pad = function (x) { return x.length < 2 ? '0' + x : x; };
    return pad(m[1]) + '.' + pad(m[2]) + '.' + (m[3].length === 2 ? '20' + m[3] : m[3]);
  }
  dateIn.addEventListener('input', function () { setAll('d', cleanDate(dateIn.value) || dateIn.placeholder); });
  form.querySelectorAll('input[name="item"]').forEach(function (r) {
    r.addEventListener('change', function () {
      stage.setAttribute('data-mode', r.value);
      if (r.value === 'tray') shine();
    });
  });

  // ===== الحجز: ننسخ التفاصيل ونفتح رسالة إنستغرام =====
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var item = form.querySelector('input[name="item"]:checked');
    var g = (groomIn.value || '').trim(), b = (brideIn.value || '').trim();
    var lines = ['مرحبًا، أودّ حجز: ' + item.getAttribute('data-label') + ' (' + item.getAttribute('data-price') + ' دينار)'];
    if (g) lines.push('اسم العريس: ' + g);
    if (b) lines.push('اسم العروس: ' + b);
    if (dateIn.value.trim()) lines.push('التاريخ: ' + cleanDate(dateIn.value));
    lines.push('من موقع salmagifts.com');
    var msg = lines.join('\n');
    var fallback = function () { toast('اكتبوا لنا الأسماء والتاريخ في رسالة إنستغرام.'); };
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(msg).then(function () {
          toast('نسخنا تفاصيل طلبكم. الصقوها في رسالة إنستغرام وأرسلوها.');
        }, fallback);
      } else { fallback(); }
    } catch (err) { fallback(); }
    var win = window.open(form.action, '_blank');
    if (win) { try { win.opener = null; } catch (err) {} }
    else { setTimeout(function () { window.location.href = form.action; }, 900); }
  });

  // زر الحجز الثابت ما بيلزم وفورم الأسماء ظاهر
  var sticky = document.querySelector('.sticky-cta');
  var heroBtn = form.querySelector('button[type=submit]');
  if (sticky && heroBtn && 'IntersectionObserver' in window) {
    // الزر الثابت يظهر بس بعد ما زر الأسماء يطلع من فوق الشاشة
    new IntersectionObserver(function (es) {
      es.forEach(function (en) { sticky.classList.toggle('away', en.isIntersecting); });
    }).observe(heroBtn);
  }
  shine();
})();
