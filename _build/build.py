# -*- coding: utf-8 -*-
"""
مولّد صفحات موقع هدايا سلمى.

كل الأسعار والنصوص الأساسية موجودة بأعلى هاد الملف (PRICES و PRODUCTS و FAQ).
بعد أي تعديل:  python3 _build/build.py
بيعيد كتابة كل صفحات الـHTML و sitemap.xml و llms.txt بالأسعار الجديدة.
(إذا عدّلت HTML يدوياً بدون هاد السكربت، تعديلك بينمسح عند التشغيل الجاي —
 فالأفضل دايماً تعدّل هون.)
"""
import json, os, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://salmagifts.com"
IG_DM = "https://ig.me/m/salma.gifts1"
IG = "https://www.instagram.com/salma.gifts1/"
FB = "https://www.facebook.com/101132472391425"
MESSENGER = "https://m.me/101132472391425"
DELIVERY = 2
TODAY = datetime.date.today().isoformat()
VERSION = "4"  # غيّره لما تعدّل style.css عشان المتصفحات تجيب النسخة الجديدة

# =====================================================================
# الأسعار — المصدر الوحيد. غيّر الرقم هون بس.
# =====================================================================
PRICES = {
    "masaka": 18,        # مسكة العروس
    "taliqa": 2,         # تعليقة للمسكة (إضافة)
    "saniya": 15,        # صينية الخطوبة / الدبل
    "bakj_berwaz": 20,   # بكج البرواز
    "bakj_asasi": 22,    # البكج الأساسي
    "bakj_shamel": 30,   # البكج الشامل
    "kitab": 9,          # كتاب / دفتر توقيع لحاله
    "mahr": 18,          # صندوق المهر
    "takharroj": 13,     # صينية التخرج
    "stand": 2, "fanajin": 5, "qassasat": 3, "taqweem": 2,
}
P = PRICES
def withdel(k): return P[k] + DELIVERY

# =====================================================================
# الصفحات
# =====================================================================
PAGES = {
    "home":  {"path": "/", "nav": "الرئيسية"},
    "masakat": {"path": "/masakat-arayes/", "nav": "مسكات العرائس"},
    "sawani": {"path": "/sawani-khotoba/", "nav": "صواني الخطوبة"},
    "bakjat": {"path": "/bakjat-katb-ktab/", "nav": "بكجات كتب الكتاب"},
    "mahr": {"path": "/sandouq-mahr/", "nav": "صندوق المهر"},
    "grad": {"path": "/hadaya-takharroj/", "nav": "هدايا التخرج"},
    "tawseel": {"path": "/tawseel/", "nav": "الأسعار والتوصيل"},
    "faq": {"path": "/as2ila/", "nav": "أسئلة شائعة"},
}
NAV_ORDER = ["masakat", "sawani", "bakjat", "mahr", "grad", "tawseel", "faq"]

# =====================================================================
# الأسئلة الشائعة — نفس صيغة سؤال الناس
# =====================================================================
FAQ = [
    ("من أين أشتري مسكة عروس في الأردن؟",
     f"من هدايا سلمى، حيث نجهّز مسكات العرائس بتصاميم متعددة بسعر {P['masaka']} دينارًا، ونوصلها إلى جميع محافظات الأردن مقابل {DELIVERY} دينار. يتم الطلب برسالة على إنستغرام salma.gifts1."),
    ("كم سعر مسكة العروس؟",
     f"سعرها {P['masaka']} دينارًا، و{withdel('masaka')} دينارًا شاملة التوصيل. ويمكن إضافة تعليقة تحمل اسمَي العروسين والتاريخ مقابل {P['taliqa']} دينار."),
    ("هل ورد المسكة طبيعي أم صناعي؟",
     "ورد صناعي عالي الجودة لا يذبل، فتبقى المسكة ذكرى دائمة. وتضم كل مسكة ما بين 20 و25 وردة."),
    ("كم سعر صينية الخطوبة؟",
     f"سعرها {P['saniya']} دينارًا، و{withdel('saniya')} دينارًا شاملة التوصيل. وتأتي مع علبتين للخواتم تحملان الحرفين الأولين من اسمَي العروسين مجانًا، وشريط من اللؤلؤ والدانتيل، وطبقة حماية من الكسر."),
    ("ما الفرق بين البكجات؟",
     f"بكج البرواز {P['bakj_berwaz']} دينار (صينية وبرواز بصمات مع الحبر). البكج الأساسي {P['bakj_asasi']} دينار (صينية وكتاب عقد الزواج للتوقيع والبصمات مع الحبر ورسالة العمر). البكج الشامل {P['bakj_shamel']} دينار (البكج الأساسي مع الفناجين والقصاصات)."),
    ("هل تكتبون الأسماء والتاريخ؟",
     "نعم، تُجهَّز الصواني والبكجات وكتب التوقيع بأسماء العروسين والتاريخ والعبارة التي تختارونها. وتُكتب الآية على الصينية إلا إذا رغبتم في عبارة بدلًا منها."),
    ("هل توصلون إلى إربد والزرقاء والكرك والعقبة؟",
     f"نعم، نوصل إلى جميع محافظات المملكة: عمّان، والزرقاء، وإربد، والسلط، ومأدبا، وجرش، وعجلون، والمفرق، والكرك، والطفيلة، ومعان، والعقبة. وأجرة التوصيل {DELIVERY} دينار."),
    ("متى يجب أن أحجز قبل المناسبة؟",
     "يُفضَّل الحجز قبل المناسبة بثلاثة أيام على الأقل، إذ يُجهَّز الطلب ويُسلَّم خلال يومين كحد أقصى."),
    ("كيف أدفع؟",
     "الدفع عند الاستلام نقدًا أو عبر كليك مع المندوب، دون أي دفعة مسبقة."),
    ("ماذا لو لم تعجبني القطعة؟",
     f"تتوفر خدمة المعاينة عند الاستلام، فتشاهدون الطلب قبل الدفع. وإن لم يعجبكم يمكنكم إرجاعه ودفع أجرة التوصيل فقط ({DELIVERY} دينار)."),
    ("هل لديكم محل يمكن زيارته؟",
     "نعمل عبر الإنترنت ونوصل إلى جميع أنحاء الأردن، وتتم جميع الطلبات برسالة على إنستغرام أو ماسنجر."),
    ("كيف أطلب؟",
     "أرسلوا لنا رسالة على إنستغرام salma.gifts1 تتضمن المنتج والتصميم، واسمَي العروسين والتاريخ، واسم المستلم ورقم هاتفه، والمحافظة والمنطقة، وسنؤكد لكم الطلب."),
    ("هل لديكم هدايا تخرج؟",
     f"نعم، صينية تخرج باسم الخريج أو الخريجة والتخصص بسعر {P['takharroj']} دينارًا، و{withdel('takharroj')} دينارًا شاملة التوصيل."),
]

# =====================================================================
# أدوات صغيرة
# =====================================================================
E = html.escape
def img(src, alt, cls="card-img", lazy=True, w=720, h=900):
    return (f'<img class="{cls}" src="/assets/img/{src}" alt="{E(alt)}" width="{w}" height="{h}"'
            + (' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"') + '>')

IG_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8" fill="currentColor"/></svg>'

def cta(label="اطلبوا الآن على إنستغرام", cls="btn btn-gold", event="cta"):
    return f'<a class="{cls}" href="{IG_DM}" target="_blank" rel="noopener" data-event="{event}">{IG_ICON}{label}</a>'

def price_html(k, note=None):
    if note is None:
        note = f"{withdel(k)} دينار مع التوصيل"
    return f'<div class="price"><b>{P[k]} دينار</b><span>{note}</span></div>'

def faq_html(items):
    out = ['<div class="faq">']
    for q, a in items:
        out.append(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>')
    out.append('</div>')
    return "\n".join(out)

def faq_schema(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

def breadcrumb(key):
    if key == "home":
        return "", None
    p = PAGES[key]
    h = (f'<nav class="breadcrumb container" aria-label="مسار الصفحة"><ol>'
         f'<li><a href="/">الرئيسية</a></li><li aria-current="page">{E(p["nav"])}</li></ol></nav>')
    sch = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "الرئيسية", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": p["nav"], "item": SITE + p["path"]}]}
    return h, sch

STORE_ID = SITE + "/#store"
STORE = {
    "@type": "OnlineStore", "@id": STORE_ID,
    "name": "Salma Gifts - هدايا سلمى", "alternateName": ["هدايا سلمى", "Salma Gifts"],
    "url": SITE + "/", "logo": SITE + "/assets/img/logo-512.png",
    "image": SITE + "/assets/img/og-salma-gifts.jpg",
    "slogan": "لتبقى ذكرياتكم الجميلة، خالدة.",
    "description": "متجر أردني أونلاين لهدايا المناسبات حسب الطلب: مسكات العرايس، صواني الخطوبة والدبل، بكجات كتب الكتاب، صندوق المهر وهدايا التخرج، بالتوصيل لكل محافظات الأردن.",
    "areaServed": {"@type": "Country", "name": "Jordan"},
    "address": {"@type": "PostalAddress", "addressCountry": "JO"},
    "currenciesAccepted": "JOD", "paymentAccepted": "Cash, CliQ",
    "sameAs": [IG, FB],
    "contactPoint": {"@type": "ContactPoint", "contactType": "customer service",
                      "url": IG_DM, "availableLanguage": ["ar"], "areaServed": "JO"},
}

def product_schema(name, desc, images, price, avail="https://schema.org/InStock", sku=None):
    return {
        "@type": "Product", "name": name, "description": desc,
        "image": [SITE + "/assets/img/" + i for i in images],
        "brand": {"@type": "Brand", "name": "Salma Gifts - هدايا سلمى"},
        **({"sku": sku} if sku else {}),
        "offers": {
            "@type": "Offer", "price": str(price), "priceCurrency": "JOD",
            "availability": avail, "url": None, "seller": {"@id": STORE_ID},
            "shippingDetails": {
                "@type": "OfferShippingDetails",
                "shippingRate": {"@type": "MonetaryAmount", "value": str(DELIVERY), "currency": "JOD"},
                "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "JO"},
                "deliveryTime": {"@type": "ShippingDeliveryTime",
                                  "handlingTime": {"@type": "QuantitativeValue", "minValue": 0, "maxValue": 1, "unitCode": "DAY"},
                                  "transitTime": {"@type": "QuantitativeValue", "minValue": 1, "maxValue": 2, "unitCode": "DAY"}}},
        },
    }

# =====================================================================
# القالب العام (النسخة الهادئة — تشرين الأول ٢٠٢٦)
# =====================================================================
def img(src, alt, cls="", lazy=True, w=720, h=900):
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/{src}" alt="{E(alt)}" width="{w}" height="{h}"'
            + (' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"') + '>')

def cta(label="راسلونا للحجز", cls="btn btn-primary", event="cta"):
    return f'<a class="{cls}" href="{IG_DM}" target="_blank" rel="noopener" data-event="{event}">{IG_ICON}<span>{label}</span></a>'

def photo(src, alt, lazy=True, cls=""):
    return f'<figure class="photo {cls}">{img(src, alt, lazy=lazy)}</figure>'

def layout(key, title, desc, body, schemas, og_img="og-salma-gifts.jpg"):
    path = PAGES[key]["path"] if key in PAGES else "/404.html"
    canonical = SITE + path
    nav = "".join(
        f'<a href="{PAGES[k]["path"]}"' + (' aria-current="page"' if k == key else "") + f'>{E(PAGES[k]["nav"])}</a>'
        for k in NAV_ORDER)
    mnav = '<a href="/"' + (' aria-current="page"' if key == "home" else "") + '>الرئيسية</a>' + nav
    graph = [STORE, {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/",
                     "name": "هدايا سلمى - Salma Gifts", "inLanguage": "ar", "publisher": {"@id": STORE_ID}}]
    graph += [s for s in schemas if s]
    for g in graph:
        if g.get("@type") == "Product":
            g["offers"]["url"] = canonical
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    robots = '<meta name="robots" content="noindex">' if key == "404" else '<meta name="robots" content="index, follow, max-image-preview:large">'
    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ar_JO">
<meta property="og:site_name" content="هدايا سلمى - Salma Gifts">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/img/{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FBF6F3">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/el-messiri-arabic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/aref-ruqaa-700-arabic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css?v={VERSION}">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<a class="skip" href="#main">تخطَّ إلى المحتوى</a>

<!-- ===== الهيدر ===== -->
<header class="site-header">
  <div class="header-row">
    <a class="brand" href="/" aria-label="هدايا سلمى - الرئيسية">
      <img src="/assets/img/logo.webp" alt="شعار هدايا سلمى Salma Gifts" width="44" height="46">
      <span class="brand-name">هدايا سلمى</span>
    </a>
    <nav class="main-nav" aria-label="القائمة الرئيسية">{nav}</nav>
    {cta("احجزوا الآن", "btn btn-primary btn-sm header-cta", "cta_header")}
    <button class="menu-btn" type="button" aria-label="القائمة" aria-expanded="false" aria-controls="mobile-nav">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><line x1="4" x2="20" y1="8" y2="8"/><line x1="4" x2="20" y1="16" y2="16"/></svg>
    </button>
  </div>
  <nav class="mobile-nav" id="mobile-nav" aria-label="القائمة">{mnav}</nav>
</header>

<main id="main">
{body}
</main>

<!-- ===== الختام ===== -->
<section class="closing">
  <div class="container narrow">
    <p class="closing-title">هل اقترب موعد مناسبتكم؟</p>
    <p>أرسلوا لنا الأسماء والتاريخ، ونجهّز طلبكم خلال يومين.</p>
    {cta("تواصلوا معنا على إنستغرام", "btn btn-primary", "cta_closing")}
  </div>
</section>

<!-- ===== الفوتر ===== -->
<footer class="site-footer">
  <div class="footer-grid container">
    <div>
      <p class="footer-brand">هدايا سلمى</p>
      <p>لتبقى ذكرياتكم الجميلة، خالدة.<br>هدايا الخطوبة وعقد القران والتخرج، تُجهَّز حسب الطلب في الأردن وتُوصَل إلى جميع المحافظات.</p>
    </div>
    <ul>
      {"".join(f'<li><a href="{PAGES[k]["path"]}">{E(PAGES[k]["nav"])}</a></li>' for k in NAV_ORDER)}
    </ul>
    <ul>
      <li><a href="{IG}" target="_blank" rel="noopener">إنستغرام: salma.gifts1</a></li>
      <li><a href="{MESSENGER}" target="_blank" rel="noopener">ماسنجر</a></li>
      <li><a href="{FB}" target="_blank" rel="noopener">صفحة فيسبوك</a></li>
    </ul>
  </div>
  <p class="copy">© {datetime.date.today().year} Salma Gifts - هدايا سلمى، الأردن</p>
</footer>

<div class="sticky-cta">{cta("احجزوا عبر إنستغرام", "btn btn-primary btn-block", "cta_sticky")}</div>
<script src="/assets/js/main.js?v={VERSION}" defer></script>
</body>
</html>
"""

def write(path, content):
    full = os.path.join(ROOT, path.lstrip("/"))
    if full.endswith("/"):
        full += "index.html"
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

def related(exclude):
    links = "".join(f'<a href="{PAGES[k]["path"]}">{E(PAGES[k]["nav"])}</a>' for k in NAV_ORDER if k != exclude)
    return f'<nav class="related" aria-label="صفحات أخرى"><p>صفحات أخرى</p><div class="chips">{links}</div></nav>'

def promise_list():
    return f"""<ul class="promise">
  <li><b>معاينة قبل الدفع</b><span>وإن لم يعجبكم الطلب تدفعون أجرة التوصيل فقط.</span></li>
  <li><b>الدفع عند الاستلام</b><span>نقدًا أو عبر كليك.</span></li>
  <li><b>جاهز خلال يومين</b><span>يُفضَّل الحجز قبل المناسبة بثلاثة أيام.</span></li>
  <li><b>توصيل {DELIVERY} دينار</b><span>إلى أي محافظة في الأردن.</span></li>
</ul>"""

def gallery(items, cols=3):
    figs = "".join(f'<figure>{img(i, a)}<figcaption>{E(c)}</figcaption></figure>' for i, a, c in items)
    return f'<div class="gallery cols-{cols}">{figs}</div>'

def product_hero(key, h1, lead, k, image, alt, note=None, extra=""):
    bc, sch = breadcrumb(key)
    note = note or f"{withdel(k)} دينارًا شاملة التوصيل إلى أي محافظة"
    html_ = bc + f"""
<section class="p-hero container">
  <div class="p-hero-text">
    <h1>{E(h1)}</h1>
    <p class="lead">{lead}</p>
    <p class="p-price"><b>{P[k]} دينار</b><span>{E(note)}</span></p>
    {extra}
    <div class="actions">{cta("احجزوا الآن", "btn btn-primary", "cta_product")}</div>
  </div>
  {photo(image, alt, lazy=False)}
</section>"""
    return html_, sch

def section(title, inner, cls="", intro=""):
    i = f'<p class="section-intro">{intro}</p>' if intro else ""
    return f"""<section class="section {cls}"><div class="container">
  <h2>{E(title)}</h2>{i}
  {inner}
</div></section>"""

def includes(items):
    return '<ul class="includes">' + "".join(f"<li>{E(x)}</li>" for x in items) + "</ul>"

# =====================================================================
# الرئيسية
# =====================================================================
def build_home():
    cards = [
        ("masakat", "مسكة العروس", "masaka", "masaka-arous-1.webp", "مسكة عروس بيضاء من هدايا سلمى"),
        ("sawani", "صينية الخطوبة والدبل", "saniya", "saniyet-khotoba-1.webp", "صينية خطوبة بالأسماء من هدايا سلمى"),
        ("bakjat", "البكج الأساسي لكتب الكتاب", "bakj_asasi", "bakj-katb-ktab-2.webp", "البكج الأساسي لكتب الكتاب من هدايا سلمى"),
        ("bakjat", "بكج البرواز", "bakj_berwaz", "bakj-berwaz-1.webp", "بكج البرواز من هدايا سلمى"),
        ("mahr", "صندوق المهر", "mahr", "sandouq-mahr-1.webp", "صندوق مهر من هدايا سلمى"),
        ("grad", "هدية التخرج", "takharroj", "hadiyet-takharroj-1.webp", "صينية تخرج بالاسم من هدايا سلمى"),
    ]
    grid = "".join(f"""<a class="card" href="{PAGES[pg]['path']}">
  {img(im, alt)}
  <span class="card-name">{E(n)}</span>
  <span class="card-price">{P[k]} دينار</span>
</a>""" for pg, n, k, im, alt in cards)
    steps = [("اختاروا التصميم", "من الموقع أو من إنستغرام، أو أرسلوا صورة لتصميم يعجبكم."),
             ("أرسلوا الأسماء والتاريخ", "مع العنوان ورقم الهاتف."),
             ("استلموا وعاينوا", "خلال يومين، وادفعوا عند الاستلام.")]
    st = "".join(f'<li><b>{t}</b><span>{d}</span></li>' for t, d in steps)
    body = f"""
<!-- ===== الافتتاحية ===== -->
<section class="hero container">
  <div class="hero-text">
    <p class="slogan">لتبقى ذكرياتكم الجميلة، خالدة.</p>
    <h1>مسكات العرائس وصواني الخطوبة بأسمائكم</h1>
    <p class="lead">نجهّز كل قطعة على حدة، بأعلى جودة وبأسعار مناسبة، ونوصلها إلى أي محافظة في الأردن.</p>
    <div class="actions">
      {cta("احجزوا الآن", "btn btn-primary", "cta_hero")}
      <a class="btn btn-quiet" href="#collection">تصفّحوا المنتجات</a>
    </div>
  </div>
  {photo("hero-masaka-arous.webp", "مسكة عروس تيوليب بيضاء مع لولو، من تجهيز هدايا سلمى", lazy=False, cls="hero-photo")}
</section>

<!-- ===== شريط الثقة ===== -->
<section class="trust"><ul class="container">
  <li><b>+1500</b><span>طلب أنجزناه</span></li>
  <li><b>+120</b><span>طلبًا كل أسبوع</span></li>
  <li><b>معاينة ودفع</b><span>عند الاستلام</span></li>
  <li><b>توصيل</b><span>إلى جميع المحافظات</span></li>
</ul></section>

<!-- ===== المنتجات ===== -->
<section class="section" id="collection"><div class="container">
  <div class="section-head"><h2>منتجاتنا</h2><a href="{PAGES['tawseel']['path']}">كل الأسعار</a></div>
  <div class="cards">{grid}</div>
</div></section>

<!-- ===== قصتنا ===== -->
<section class="section tint"><div class="container story">
  <h2>كل قطعة تُجهَّز على حدة</h2>
  <p>لا نعمل بالجملة؛ فكل مسكة وكل صينية تُجهَّز في ورشتنا بأسمائكم وتاريخ مناسبتكم، ونراجعها قبل أن تخرج إليكم. هدفنا أن نقدّم أفضل جودة بأفضل سعر، لأن الفرحة لا ينبغي أن تكلّف فوق الطاقة.</p>
</div></section>

<!-- ===== كيف تطلبوا ===== -->
<section class="section"><div class="container">
  <h2>كيف تطلبون</h2>
  <ol class="steps">{st}</ol>
  <div class="actions">{cta("أرسلوا رسالة على إنستغرام", "btn btn-primary", "cta_steps")}</div>
</div></section>

<!-- ===== أسئلة ===== -->
<section class="section"><div class="container narrow">
  <div class="section-head"><h2>أسئلة متكررة</h2><a href="{PAGES['faq']['path']}">كل الأسئلة</a></div>
  {faq_html(FAQ[:4])}
</div></section>
"""
    title = "هدايا سلمى | مسكات عرائس وصواني خطوبة وبكجات كتب كتاب في الأردن"
    desc = f"مسكة عروس {P['masaka']} دينار، صينية خطوبة {P['saniya']} دينار، وبكجات كتب كتاب بأسمائكم، تُجهَّز كل قطعة على حدة. معاينة ودفع عند الاستلام وتوصيل إلى جميع أنحاء الأردن."
    write("/", layout("home", title, desc, body, [faq_schema(FAQ[:4])]))

# =====================================================================
# مسكات العرايس
# =====================================================================
def build_masakat():
    head, bsch = product_hero("masakat", "مسكات العرائس في الأردن",
        "ورد صناعي عالي الجودة لا يذبل، من 20 إلى 25 وردة، بتصاميم تناسب عقد القران والخطوبة والزفاف.",
        "masaka", "masaka-arous-calla.webp", "مسكة عروس كالا بيضاء من هدايا سلمى")
    models = [("masaka-arous-1.webp", "مسكة ورد أبيض مع جبسوفيل", "ورد أبيض وجبسوفيل"),
              ("masaka-arous-trend.webp", "مسكة تيوليب مع لولو", "تيوليب مع لولو"),
              ("masaka-arous-pink.webp", "مسكة وردي وأبيض", "وردي وأبيض"),
              ("masaka-arous-3.webp", "مسكة كالا طويلة", "كالا طويلة"),
              ("masaka-arous-tulip.webp", "مسكة تيوليب بقاعدة ستراس", "تيوليب بقاعدة ستراس"),
              ("masaka-arous-2.webp", "مسكات كالا بقاعدة لولو", "كالا بقاعدة لولو")]
    faqs = [FAQ[0], FAQ[1], FAQ[2], FAQ[7], FAQ[9]]
    body = head + section("تصاميم المسكات", gallery([(i, a + "، من هدايا سلمى", c) for i, a, c in models]),
        intro="جميعها بالسعر نفسه. وإن أعجبكم تصميم غير موجود هنا، أرسلوا لنا صورته.") + f"""
<section class="section tint"><div class="container split">
  <div>
    <h2>تعليقة بأسمائكم</h2>
    <p>يمكن إضافة تعليقة من الأكريليك إلى المسكة، تحمل اسمَي العريس والعروس وتاريخ المناسبة.</p>
    <p class="p-price"><b>+{P['taliqa']} دينار</b><span>المسكة مع التعليقة والتوصيل: {P['masaka'] + P['taliqa'] + DELIVERY} دينارًا</span></p>
  </div>
  {photo("masaka-arous-4.webp", "مسكة عروس تيوليب مع تعليقة أكريليك، من هدايا سلمى", cls="small")}
</div></section>
{section("قبل الحجز", promise_list())}
<section class="section"><div class="container narrow">
  <h2>أسئلة عن مسكات العرائس</h2>
  {faq_html(faqs)}
  {related("masakat")}
</div></section>"""
    sch = [bsch, faq_schema(faqs),
           product_schema("مسكة العروس", "مسكة عروس من الورد الصناعي عالي الجودة، 20 إلى 25 وردة، بموديلات وألوان متعددة.",
                          ["masaka-arous-calla.webp", "masaka-arous-1.webp", "masaka-arous-trend.webp"], P["masaka"], sku="masaka")]
    write(PAGES["masakat"]["path"], layout("masakat",
        f"مسكة عروس في الأردن بسعر {P['masaka']} دينار | هدايا سلمى",
        f"مسكات عرائس من ورد صناعي عالي الجودة بتصاميم متعددة، {P['masaka']} دينار و{withdel('masaka')} مع التوصيل لكل محافظات الأردن. معاينة ودفع عند الاستلام.",
        body, sch, og_img="masaka-arous-calla.webp"))

# =====================================================================
# صواني الخطوبة
# =====================================================================
def build_sawani():
    head, bsch = product_hero("sawani", "صواني خطوبة ودبل بالأسماء",
        "مرآة تحمل أسماءكم وتاريخ المناسبة، مع علبتين للخواتم بحروفكم الأولى، ولؤلؤ ودانتيل.",
        "saniya", "saniyet-khotoba-1.webp", "صينية خطوبة من المرآة بالأسماء مع علب الدبل، من هدايا سلمى")
    faqs = [FAQ[3], FAQ[5], FAQ[6], FAQ[7], FAQ[9]]
    adds = f"""<table class="prices"><tbody>
      <tr><td>حروفكم الأولى على علب الدبل</td><td>مجانًا</td></tr>
      <tr><td>ستاند أسود</td><td>+{P['stand']} دينار</td></tr>
      <tr><td>قصاصات</td><td>+{P['qassasat']} دنانير</td></tr>
      <tr><td>فناجين بالأسماء</td><td>+{P['fanajin']} دنانير</td></tr>
      <tr><td>قصاصة التقويم أو رسالة العمر</td><td>+{P['taqweem']} دينار</td></tr>
    </tbody></table>"""
    body = head + section("تصاميم الصواني", gallery([
            ("saniyet-khotoba-2.webp", "صينية دبل بالحروف والتاريخ", "بالحروف والتاريخ"),
            ("saniyet-khotoba-3.webp", "صينية دبل مع ورد ولؤلؤ", "مع ورد ولؤلؤ"),
            ("bakj-berwaz-2.webp", "صينية دبل بإطار من اللؤلؤ", "بإطار من اللؤلؤ")])) + f"""
<section class="section tint"><div class="container split">
  <div><h2>ماذا تتضمن</h2>{includes(["مرآة بأسمائكم وتاريخ المناسبة", "آية، أو عبارة بدلًا منها حسب رغبتكم", "علبتان للخواتم بحروفكم الأولى", "شريط من اللؤلؤ والدانتيل بين الخواتم", "طبقة حماية من الكسر"])}</div>
  <div><h2>إضافات</h2>{adds}</div>
</div></section>
<section class="section"><div class="container narrow">
  <h2>هل تريدون الصينية مع كتاب عقد القران؟</h2>
  <p>اطلبوها ضمن بكج: بكج البرواز بسعر {P['bakj_berwaz']} دينار، أو البكج الأساسي بسعر {P['bakj_asasi']} دينارًا مع كتاب التوقيع والبصمات ورسالة العمر.</p>
  <p><a class="btn btn-quiet" href="{PAGES['bakjat']['path']}">تصفّحوا البكجات</a></p>
</div></section>
<section class="section"><div class="container narrow">
  <h2>أسئلة عن صواني الخطوبة</h2>
  {faq_html(faqs)}
  {related("sawani")}
</div></section>"""
    sch = [bsch, faq_schema(faqs),
           product_schema("صينية الخطوبة والدبل", "صينية من المرآة بأسماء العروسين والتاريخ مع علبتين للخواتم ولؤلؤ ودانتيل وطبقة حماية من الكسر.",
                          ["saniyet-khotoba-1.webp", "saniyet-khotoba-2.webp", "saniyet-khotoba-3.webp"], P["saniya"], sku="saniya")]
    write(PAGES["sawani"]["path"], layout("sawani",
        f"صينية خطوبة ودبل بالأسماء بسعر {P['saniya']} دينار | هدايا سلمى",
        f"صواني خطوبة ودبل من المرآة بأسماء العروسين والتاريخ مع علب الخواتم. {P['saniya']} دينار و{withdel('saniya')} مع التوصيل لكل الأردن، معاينة ودفع عند الاستلام.",
        body, sch, og_img="saniyet-khotoba-1.webp"))

# =====================================================================
# البكجات
# =====================================================================
def build_bakjat():
    bc, bsch = breadcrumb("bakjat")
    def pkg(name, k, desc, inc, tag=""):
        t = f' <span class="tag">{E(tag)}</span>' if tag else ""
        return f"""<article class="pkg">
  <h3>{E(name)}{t}</h3>
  <p class="p-price"><b>{P[k]} دينار</b><span>{withdel(k)} شاملة التوصيل</span></p>
  <p>{E(desc)}</p>
  {includes(inc)}
</article>"""
    pkgs = (pkg("بكج البرواز", "bakj_berwaz", "لمن يفضّل برواز بصمات يُعلَّق في المنزل بدلًا من الكتاب.", ["صينية الدبل بأسمائكم", "علب الخواتم بأحرفكم", "برواز بصمات بالأسماء", "حبر البصمات"])
            + pkg("البكج الأساسي", "bakj_asasi", "الأكثر طلبًا لعقد القران، ويضم كل ما تحتاجونه.", ["صينية الدبل بأسمائكم", "علب الخواتم بأحرفكم", "كتاب عقد الزواج والتوقيع والبصمات", "حبر البصمات", "رسالة العمر", "شريط لؤلؤ بين الخواتم"], tag="الأكثر طلبًا")
            + pkg("البكج الشامل", "bakj_shamel", "البكج الأساسي كاملًا، مع الفناجين والقصاصات.", ["كل محتويات البكج الأساسي", "فناجين بالأسماء", "قصاصات"]))
    faqs = [FAQ[4], FAQ[5], FAQ[7], FAQ[8], FAQ[9]]
    body = bc + f"""
<section class="p-hero container">
  <div class="p-hero-text">
    <h1>بكجات كتب الكتاب: محتوياتها وأسعارها</h1>
    <p class="lead">كل ما تحتاجونه لعقد القران في طلب واحد، بأسمائكم وتاريخ مناسبتكم، من {P['bakj_berwaz']} إلى {P['bakj_shamel']} دينارًا.</p>
    <div class="actions">{cta("احجزوا الآن", "btn btn-primary", "cta_product")}</div>
  </div>
  {photo("bakj-katb-ktab-2.webp", "البكج الأساسي لكتب الكتاب: صينية دبل وكتاب توقيع وبصمات، من هدايا سلمى", lazy=False)}
</section>
<section class="section"><div class="container">
  <h2>اختاروا البكج المناسب</h2>
  <div class="pkgs">{pkgs}</div>
  <p class="section-intro">وإن أردتم كتاب التوقيع والبصمات وحده، فسعره {P['kitab']} دنانير، و{withdel('kitab')} دينارًا شاملة التوصيل.</p>
</div></section>
{section("من أعمالنا", gallery([("bakj-katb-ktab-1.webp", "كتاب عقد الزواج بالأسماء", "كتاب عقد الزواج"), ("bakj-berwaz-1.webp", "بكج البرواز مع صينية الدبل", "بكج البرواز"), ("bakj-berwaz-3.webp", "برواز البصمات بالأسماء", "برواز البصمات")]))}
{section("قبل الحجز", promise_list(), cls="tint")}
<section class="section"><div class="container narrow">
  <h2>أسئلة عن بكجات عقد القران</h2>
  {faq_html(faqs)}
  {related("bakjat")}
</div></section>"""
    sch = [bsch, faq_schema(faqs),
           product_schema("بكج البرواز لكتب الكتاب", "صينية دبل مع برواز بصمات بالأسماء وحبر البصمات.", ["bakj-berwaz-1.webp", "bakj-berwaz-3.webp"], P["bakj_berwaz"], sku="bakj-berwaz"),
           product_schema("البكج الأساسي لكتب الكتاب", "صينية دبل وكتاب عقد الزواج والتوقيع والبصمات مع الحبر ورسالة العمر.", ["bakj-katb-ktab-2.webp", "bakj-katb-ktab-1.webp"], P["bakj_asasi"], sku="bakj-asasi"),
           product_schema("البكج الشامل لكتب الكتاب", "البكج الأساسي مع فناجين وقصاصات.", ["bakj-katb-ktab-1.webp"], P["bakj_shamel"], sku="bakj-shamel"),
           product_schema("كتاب توقيع وبصمات", "كتاب للتوقيع والبصمات بأسماء العروسين وتاريخ كتب الكتاب.", ["bakj-katb-ktab-1.webp"], P["kitab"], sku="kitab")]
    write(PAGES["bakjat"]["path"], layout("bakjat",
        f"بكج كتب الكتاب من {P['bakj_berwaz']} دينار | هدايا سلمى",
        f"بكجات كتب كتاب بالأسماء: بكج البرواز {P['bakj_berwaz']}، الأساسي {P['bakj_asasi']}، الشامل {P['bakj_shamel']} دينار. صينية دبل وكتاب بصمات ورسالة العمر، توصيل لكل الأردن.",
        body, sch, og_img="bakj-katb-ktab-2.webp"))

# =====================================================================
# صندوق المهر
# =====================================================================
def build_mahr():
    head, bsch = product_hero("mahr", "صندوق المهر: أجمل طريقة لتقديم المهر للعروس",
        "صندوق فاخر بكامل زينته لتقديم المهر للعروس، ويمكن إضافة الأسماء أو عبارة عليه.",
        "mahr", "sandouq-mahr-1.webp", "صندوق مهر خشبي فاخر لتقديم المهر للعروس، من هدايا سلمى",
        extra='<p class="tag">الكمية محدودة، تواصلوا معنا للتأكد من التوفر</p>')
    faqs = [("كم سعر صندوق المهر؟", f"سعره {P['mahr']} دينارًا، و{withdel('mahr')} دينارًا شاملة التوصيل إلى جميع محافظات الأردن. الكمية محدودة، لذا تواصلوا معنا للتأكد من التوفر."),
            FAQ[6], FAQ[8], FAQ[9]]
    body = head + section("قبل الحجز", promise_list(), cls="tint") + f"""
<section class="section"><div class="container narrow">
  <h2>أسئلة عن صندوق المهر</h2>
  {faq_html(faqs)}
  {related("mahr")}
</div></section>"""
    sch = [bsch, faq_schema(faqs),
           product_schema("صندوق المهر", "صندوق فاخر لتقديم المهر للعروس، شامل كامل الزينة والإكسسوارات.", ["sandouq-mahr-1.webp"], P["mahr"],
                          avail="https://schema.org/LimitedAvailability", sku="mahr")]
    write(PAGES["mahr"]["path"], layout("mahr",
        f"صندوق المهر بسعر {P['mahr']} دينار | هدايا سلمى",
        f"صندوق مهر فاخر لتقديم المهر للعروس مع كامل الزينة، {P['mahr']} دينار و{withdel('mahr')} مع التوصيل لكل محافظات الأردن. حسب التوفر.",
        body, sch, og_img="sandouq-mahr-1.webp"))

# =====================================================================
# التخرج
# =====================================================================
def build_grad():
    head, bsch = product_hero("grad", "هدايا تخرج بالاسم: صينية التخرج",
        "صينية باسم الخريج أو الخريجة والتخصص، مع ورد وزينة.",
        "takharroj", "hadiyet-takharroj-1.webp", "صينية تخرج باسم الخريجة والتخصص، من هدايا سلمى")
    faqs = [FAQ[12], FAQ[6], FAQ[7], FAQ[8], FAQ[9]]
    body = head + f"""
<section class="section"><div class="container narrow">
  <h2>ما الذي نحتاجه منكم</h2>
  {includes(["اسم الخريج أو الخريجة كما تريدون كتابته", "التخصص", "اسم المستلم ورقم الهاتف والمحافظة"])}
</div></section>
{section("قبل الحجز", promise_list(), cls="tint")}
<section class="section"><div class="container narrow">
  <h2>أسئلة عن هدايا التخرج</h2>
  {faq_html(faqs)}
  {related("grad")}
</div></section>"""
    sch = [bsch, faq_schema(faqs),
           product_schema("صينية التخرج", "صينية تخرج باسم الخريج أو الخريجة والتخصص.", ["hadiyet-takharroj-1.webp"], P["takharroj"], sku="takharroj")]
    write(PAGES["grad"]["path"], layout("grad",
        f"هدية تخرج بالاسم: صينية تخرج بسعر {P['takharroj']} دينار | هدايا سلمى",
        f"صينية تخرج باسم الخريج أو الخريجة والتخصص، {P['takharroj']} دينار و{withdel('takharroj')} مع التوصيل لكل محافظات الأردن. معاينة ودفع عند الاستلام.",
        body, sch, og_img="hadiyet-takharroj-1.webp"))

# =====================================================================
# الأسعار والتوصيل
# =====================================================================
def build_tawseel():
    bc, bsch = breadcrumb("tawseel")
    rows = [("مسكة العروس", "masaka", PAGES["masakat"]["path"]), ("صينية الخطوبة / الدبل", "saniya", PAGES["sawani"]["path"]),
            ("بكج البرواز", "bakj_berwaz", PAGES["bakjat"]["path"]), ("البكج الأساسي", "bakj_asasi", PAGES["bakjat"]["path"]),
            ("البكج الشامل", "bakj_shamel", PAGES["bakjat"]["path"]), ("كتاب أو دفتر توقيع منفرد", "kitab", PAGES["bakjat"]["path"]),
            ("صندوق المهر (حسب التوفر)", "mahr", PAGES["mahr"]["path"]), ("صينية التخرج", "takharroj", PAGES["grad"]["path"])]
    tr = "".join(f'<tr><td><a href="{u}">{E(n)}</a></td><td>{P[k]} دينار</td><td>{withdel(k)} دينار</td></tr>' for n, k, u in rows)
    adds = [("تعليقة للمسكة", "taliqa"), ("ستاند أسود", "stand"), ("قصاصات", "qassasat"), ("فناجين", "fanajin"), ("قصاصة التقويم أو رسالة العمر", "taqweem")]
    ta = "".join(f"<tr><td>{E(n)}</td><td>+{P[k]} دينار</td></tr>" for n, k in adds)
    govs = "عمّان، الزرقاء، إربد، السلط، مأدبا، جرش، عجلون، المفرق، الكرك، الطفيلة، معان، العقبة"
    body = bc + f"""
<section class="page-head container narrow">
  <h1>الأسعار، التوصيل وطريقة الطلب</h1>
  <p class="lead">لا توجد سلة مشتريات ولا دفع إلكتروني؛ تتم جميع الطلبات برسالة على إنستغرام أو ماسنجر، والدفع عند الاستلام بعد معاينة الطلب.</p>
</section>
<section class="section"><div class="container narrow">
  <h2>كل الأسعار</h2>
  <table class="prices"><thead><tr><th>المنتج</th><th>السعر</th><th>شاملًا التوصيل</th></tr></thead><tbody>{tr}</tbody></table>
  <h3>الإضافات</h3>
  <table class="prices"><tbody>{ta}<tr><td>حروفكم الأولى على علب الدبل</td><td>مجانًا</td></tr></tbody></table>
</div></section>
<section class="section tint"><div class="container narrow">
  <h2>التوصيل والدفع</h2>
  {promise_list()}
  <p class="section-intro">نوصل إلى جميع المحافظات: {govs}.</p>
</div></section>
<section class="section"><div class="container narrow">
  <h2>ماذا تكتبون في الرسالة</h2>
  {includes(["المنتج والتصميم، أو صورة التصميم", "أسماء العروسين والتاريخ، أو اسم الخريج والتخصص", "اسم المستلم ورقم الهاتف", "المحافظة والمنطقة، واليوم المناسب للاستلام"])}
  <div class="actions">{cta("أرسلوا رسالة على إنستغرام", "btn btn-primary", "cta_order")}</div>
  {related("tawseel")}
</div></section>"""
    write(PAGES["tawseel"]["path"], layout("tawseel",
        "الأسعار والتوصيل وطريقة الطلب | هدايا سلمى",
        f"أسعار مسكات العرائس وصواني الخطوبة والبكجات، والتوصيل لكل محافظات الأردن بسعر {DELIVERY} دينار خلال يومين. دفع ومعاينة عند الاستلام.",
        body, [bsch]))

# =====================================================================
# الأسئلة الشائعة
# =====================================================================
def build_faq():
    bc, bsch = breadcrumb("faq")
    body = bc + f"""
<section class="page-head container narrow">
  <h1>أسئلة شائعة عن هدايا سلمى</h1>
  <p class="lead">أكثر الأسئلة التي تصلنا عن المسكات والصواني والبكجات والأسعار والتوصيل. إن لم تجدوا سؤالكم هنا، تواصلوا معنا على إنستغرام.</p>
</section>
<section class="section"><div class="container narrow">
  {faq_html(FAQ)}
  {related("faq")}
</div></section>"""
    write(PAGES["faq"]["path"], layout("faq",
        "أسئلة شائعة: أسعار المسكات والصواني والتوصيل | هدايا سلمى",
        "من أين أشتري مسكة عروس في الأردن؟ كم سعر صينية الخطوبة؟ هل يصل التوصيل إلى جميع المحافظات؟ جميع الإجابات عن هدايا سلمى في مكان واحد.",
        body, [bsch, faq_schema(FAQ)]))

# =====================================================================
# 404
# =====================================================================
def build_404():
    body = f"""<section class="page-head container narrow">
  <h1>الصفحة غير موجودة</h1>
  <p class="lead">ربما تغيّر الرابط. عودوا إلى الصفحة الرئيسية أو اختاروا إحدى الصفحات أدناه.</p>
  <p><a class="btn btn-quiet" href="/">الرئيسية</a></p>
  {related(None)}
</section>"""
    PAGES["404"] = {"path": "/404.html", "nav": "404"}
    out = layout("404", "الصفحة غير موجودة | هدايا سلمى", "الصفحة المطلوبة غير موجودة.", body, [])
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(out)
    del PAGES["404"]

# =====================================================================
# sitemap + llms.txt
# =====================================================================
def build_sitemap():
    urls = "".join(f"  <url><loc>{SITE}{PAGES[k]['path']}</loc><lastmod>{TODAY}</lastmod></url>\n" for k in ["home"] + NAV_ORDER)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')

def build_llms():
    lines = [
        "# Salma Gifts - هدايا سلمى",
        "",
        "> متجر أردني أونلاين لهدايا المناسبات حسب الطلب: مسكات العرايس، صواني الخطوبة والدبل، بكجات كتب الكتاب، صندوق المهر وهدايا التخرج. توصيل لكل محافظات الأردن، ومعاينة ودفع عند الاستلام. الطلب عبر رسائل إنستغرام @salma.gifts1.",
        "",
        "Salma Gifts is an online gift shop in Jordan making personalized engagement and wedding items: bridal bouquets, engagement ring trays with names, marriage-contract (katb el-kitab) signature book packages, dowry (mahr) boxes and graduation gifts. Delivery to all governorates of Jordan for 2 JOD. Cash on delivery with inspection before paying. Orders via Instagram DM @salma.gifts1.",
        "",
        "## الأسعار (دينار أردني، بدون التوصيل)",
        f"- مسكة العروس: {P['masaka']} (ورد صناعي عالي الجودة، 20–25 وردة). تعليقة بالأسماء والتاريخ: +{P['taliqa']}",
        f"- صينية الخطوبة / الدبل بالأسماء: {P['saniya']}",
        f"- بكج البرواز (صينية + برواز بصمات): {P['bakj_berwaz']}",
        f"- البكج الأساسي (صينية + كتاب توقيع وبصمات + رسالة العمر + حبر): {P['bakj_asasi']}",
        f"- البكج الشامل (الأساسي + فناجين + قصاصات): {P['bakj_shamel']}",
        f"- كتاب / دفتر توقيع منفرد: {P['kitab']}",
        f"- صندوق المهر (حسب التوفر): {P['mahr']}",
        f"- صينية التخرج بالاسم والتخصص: {P['takharroj']}",
        f"- التوصيل لأي محافظة: {DELIVERY}",
        "",
        "## السياسات",
        "- الطلب يجهز ويوصل خلال يومين كحد أقصى، والحجز قبل المناسبة بثلاثة أيام على الأقل.",
        "- الدفع عند الاستلام (كاش أو كليك)، مع معاينة قبل الدفع؛ إذا لم يعجب الطلب يُرجع ويُدفع التوصيل فقط.",
        "- أونلاين فقط، لا يوجد محل. لا يوجد واتساب؛ التواصل عبر إنستغرام أو ماسنجر.",
        "",
        "## الصفحات",
    ] + [f"- [{PAGES[k]['nav']}]({SITE}{PAGES[k]['path']})" for k in ["home"] + NAV_ORDER] + [
        "",
        "## التواصل",
        f"- إنستغرام: {IG} (رسالة مباشرة: {IG_DM})",
        f"- فيسبوك: {FB} · ماسنجر: {MESSENGER}",
    ]
    with open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

if __name__ == "__main__":
    build_home(); build_masakat(); build_sawani(); build_bakjat(); build_mahr(); build_grad()
    build_tawseel(); build_faq(); build_404(); build_sitemap(); build_llms()
    print("تم بناء الموقع.")
