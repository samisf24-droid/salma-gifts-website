// هدايا سلمى — سكربت صغير لفتح وإغلاق القائمة على الموبايل فقط.
// كل محتوى الموقع مكتوب بالـHTML، وهاد الملف ما بيولّد أي نص.
(function () {
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('mobile-nav');
  if (!btn || !nav) return;
  btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
})();
