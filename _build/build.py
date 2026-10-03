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
VERSION = "1"  # غيّره لما تعدّل style.css عشان المتصفحات تجيب النسخة الجديدة

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
    "masakat": {"path": "/masakat-arayes/", "nav": "مسكات العرايس"},
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
    ("من وين أشتري مسكة عروس بالأردن؟",
     f"من هدايا سلمى. عنا مسكات عرايس بموديلات متعددة بسعر {P['masaka']} دينار، والتوصيل لكل محافظات الأردن بسعر {DELIVERY} دينار. الطلب برسالة على إنستغرام salma.gifts1."),
    ("قديش سعر مسكة العروس؟",
     f"{P['masaka']} دينار، و{withdel('masaka')} دينار مع التوصيل. وإذا بدكم تعليقة عليها أسماء العروسين والتاريخ بتزيد {P['taliqa']} دينار."),
    ("المسكة ورد طبيعي ولا صناعي؟",
     "ورد صناعي عالي الجودة، بيضل معكم ذكرى وما بيذبل، وفيها من 20 لـ25 وردة."),
    ("قديش سعر صينية الخطوبة؟",
     f"{P['saniya']} دينار، و{withdel('saniya')} مع التوصيل. بتيجي مع علبتين للخواتم وعليهم أحرف العروسين مجاناً، وشبر لولو ودانتيل بين الخواتم، وطبقة حماية من الكسر."),
    ("شو الفرق بين البكجات؟",
     f"بكج البرواز {P['bakj_berwaz']} دينار (صينية + برواز بصمات مع الحبر). البكج الأساسي {P['bakj_asasi']} دينار (صينية + كتاب عقد الزواج والتوقيع والبصمات مع الحبر + رسالة العمر). البكج الشامل {P['bakj_shamel']} دينار (الأساسي + فناجين + قصاصات)."),
    ("بتكتبوا الأسماء والتاريخ؟",
     "أكيد. الصواني والبكجات وكتب التوقيع بتنعمل بأسماء العروسين والتاريخ والعبارة اللي بتختاروها. والآية موجودة على الصينية إلا إذا بدكم عبارة بدالها."),
    ("بتوصلوا لإربد والزرقاء والكرك والعقبة؟",
     f"إيه، منوصّل لكل محافظات المملكة: عمّان، الزرقاء، إربد، السلط، مأدبا، جرش، عجلون، المفرق، الكرك، الطفيلة، معان والعقبة. أجرة التوصيل {DELIVERY} دينار."),
    ("قديش لازم أحجز قبل المناسبة؟",
     "الأفضل تحجزوا قبل المناسبة بثلاثة أيام على الأقل. الطلب بيجهز وبيوصل خلال يومين كحد أقصى."),
    ("كيف بدفع؟",
     "الدفع عند الاستلام، كاش أو كليك مع المندوب. ما في أي دفع مسبق."),
    ("إذا ما عجبتني القطعة؟",
     f"في معاينة عند الاستلام. بتشوفوا الطلب قبل ما تدفعوا، وإذا ما عجبكم بترجعوه وبتدفعوا أجرة التوصيل بس ({DELIVERY} دينار)."),
    ("عندكم محل بقدر أزوره؟",
     "إحنا أونلاين، ومنوصّل لكل الأردن. كل الطلبات برسالة على إنستغرام أو ماسنجر."),
    ("كيف بطلب؟",
     "ابعتولنا رسالة على إنستغرام salma.gifts1 فيها المنتج والموديل، أسماء العروسين والتاريخ، اسم المستلم ورقم الهاتف، والمحافظة والمنطقة. منأكدلكم الطلب برسالة."),
    ("عندكم هدايا تخرج؟",
     f"إيه، صينية تخرج باسم الخريج أو الخريجة والتخصص بسعر {P['takharroj']} دينار، و{withdel('takharroj')} مع التوصيل."),
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
# القالب العام
# =====================================================================
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
    for g in graph:  # اربط عروض المنتجات برابط الصفحة
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
<meta name="theme-color" content="#FBF7F0">
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
      <img src="/assets/img/logo.webp" alt="شعار هدايا سلمى Salma Gifts" width="46" height="48">
      <span class="brand-name"><b>هدايا سلمى</b><span>SALMA GIFTS</span></span>
    </a>
    <nav class="main-nav" aria-label="القائمة الرئيسية">{nav}</nav>
    {cta("للحجز راسلونا", "btn btn-gold header-cta", "cta_header")}
    <button class="menu-btn" type="button" aria-label="القائمة" aria-expanded="false" aria-controls="mobile-nav">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="4" x2="20" y1="7" y2="7"/><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="17" y2="17"/></svg>
    </button>
  </div>
  <nav class="mobile-nav" id="mobile-nav" aria-label="القائمة">{mnav}</nav>
</header>

<main id="main">
{body}
</main>

<!-- ===== الشريط الذهبي ===== -->
<section class="cta-band">
  <div class="container">
    <h2>ألف مبروك مقدماً. احكولنا شو بدكم.</h2>
    {cta("راسلونا على إنستغرام", "btn", "cta_band")}
  </div>
</section>

<!-- ===== الفوتر ===== -->
<footer class="site-footer">
  <div class="footer-grid">
    <div>
      <b>هدايا سلمى</b>
      <p>هدايا مناسبات حسب الطلب، بالتوصيل لكل محافظات الأردن.<br>«لتبقى ذكرياتكم الجميلة، خالدة.»</p>
    </div>
    <ul>
      {"".join(f'<li><a href="{PAGES[k]["path"]}">{E(PAGES[k]["nav"])}</a></li>' for k in NAV_ORDER)}
    </ul>
    <ul>
      <li><a href="{IG}" target="_blank" rel="noopener">إنستغرام @salma.gifts1</a></li>
      <li><a href="{MESSENGER}" target="_blank" rel="noopener">ماسنجر Salma Gifts</a></li>
      <li><a href="{FB}" target="_blank" rel="noopener">صفحة فيسبوك</a></li>
    </ul>
  </div>
  <p class="copy">© {datetime.date.today().year} Salma Gifts - هدايا سلمى · الأردن</p>
</footer>

<div class="sticky-cta">{cta("للحجز راسلونا على إنستغرام", "btn btn-gold btn-block", "cta_sticky")}</div>
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

def info_boxes(custom):
    return f"""<section class="section"><div class="container"><div class="grid grid-info">
  <div class="info"><h2>التخصيص</h2><ul>{"".join(f"<li>{E(x)}</li>" for x in custom)}</ul></div>
  <div class="info"><h2>التوصيل والحجز</h2><ul>
    <li>بيجهز وبيوصل خلال يومين كحد أقصى.</li>
    <li>توصيل لكل محافظات الأردن بسعر {DELIVERY} دينار.</li>
    <li>معاينة ودفع عند الاستلام (كاش أو كليك).</li>
    <li>الحجز قبل المناسبة بثلاثة أيام على الأقل.</li>
  </ul><p class="small" style="margin-top:10px"><a href="{PAGES['tawseel']['path']}">كل الأسعار وتفاصيل التوصيل ←</a></p></div>
</div></div></section>"""

def related(exclude):
    links = "".join(f'<a href="{PAGES[k]["path"]}">{E(PAGES[k]["nav"])}</a>' for k in NAV_ORDER if k != exclude)
    return f'<div class="chips">{links}</div>'

def product_card(name, k, image, alt, desc="", contents=None, badge=None, note=None, event="cta_product", h="h2"):
    c = ""
    if contents:
        c = '<ul class="contents">' + "".join(f"<li>{E(x)}</li>" for x in contents) + "</ul>"
    b = f'<span class="badge">{E(badge)}</span>' if badge else ""
    d = f"<p>{E(desc)}</p>" if desc else ""
    return f"""<div class="card">
  {img(image, alt)}
  <div class="card-body">
    <{h} class="card-title">{E(name)}</{h}>
    {price_html(k, note)}
    {b}{d}{c}
    {cta("اطلبوها على إنستغرام", "btn btn-gold btn-block", event)}
  </div>
</div>"""

def page_head(key, h1, lead):
    bc, sch = breadcrumb(key)
    return bc + f"""
<div class="container page-head">
  <h1>{E(h1)}</h1>
  <p class="lead">{lead}</p>
</div>""", sch

# =====================================================================
# الرئيسية
# =====================================================================
def build_home():
    cards = [
        ("masakat", "مسكة العروس", "masaka", "masaka-arous-1.webp", "مسكة عروس بيضاء من الورد الصناعي على طاولة خشب — هدايا سلمى"),
        ("sawani", "صينية الخطوبة والدبل", "saniya", "saniyet-khotoba-1.webp", "صينية خطوبة مراية بالأسماء مع علب الدبل — هدايا سلمى"),
        ("bakjat", "البكج الأساسي لكتب الكتاب", "bakj_asasi", "bakj-katb-ktab-2.webp", "بكج كتب كتاب: صينية دبل وكتاب عقد زواج وبصمات — هدايا سلمى"),
        ("bakjat", "بكج البرواز", "bakj_berwaz", "bakj-berwaz-1.webp", "بكج البرواز: صينية دبل وبرواز بصمات بالأسماء — هدايا سلمى"),
        ("mahr", "صندوق المهر", "mahr", "sandouq-mahr-1.webp", "صندوق مهر خشبي فاخر لتقديم المهر للعروس — هدايا سلمى"),
        ("grad", "هدية التخرج", "takharroj", "hadiyet-takharroj-1.webp", "صينية تخرج باسم الخريجة والتخصص — هدايا سلمى"),
    ]
    card_html = "".join(f"""<a class="card" href="{PAGES[pg]['path']}">
  {img(im, alt)}
  <div class="card-body"><h3 class="card-title">{E(n)}</h3>{price_html(k)}</div>
</a>""" for pg, n, k, im, alt in cards)
    gallery = [("masaka-arous-calla.webp", "مسكة عروس كالا بيضاء"), ("saniyet-khotoba-2.webp", "صينية دبل بالأسماء والتاريخ"),
               ("masaka-arous-pink.webp", "مسكة عروس وردي وأبيض"), ("bakj-katb-ktab-1.webp", "كتاب عقد زواج وتوقيع بالأسماء"),
               ("masaka-arous-trend.webp", "مسكة عروس تيوليب مع لولو"), ("bakj-berwaz-2.webp", "صينية دبل بالأحرف ولولو")]
    gal = "".join(f'<figure class="thumb">{img(i, a)}</figure>' for i, a in gallery)
    steps = [("1", "اختاروا الموديل", "من الصور بالموقع، أو ابعتولنا صورة موديل عاجبكم ومنأكدلكم التوفر."),
             ("2", "ابعتوا التفاصيل برسالة", "الأسماء والتاريخ، اسم المستلم ورقم الهاتف، والمحافظة والمنطقة."),
             ("3", "استلموا، عاينوا، وادفعوا", "منجهز الطلب ومنوصله خلال يومين، والدفع بعد المعاينة.")]
    st = "".join(f'<li class="step"><span class="step-n">{n}</span><b>{t}</b><span>{d}</span></li>' for n, t, d in steps)
    body = f"""
<!-- ===== الهيرو ===== -->
<section class="hero">
  <picture>
    <source media="(min-width: 900px)" srcset="/assets/img/hero-masaka-arous-wide.webp">
    <img class="hero-img" src="/assets/img/hero-masaka-arous.webp" alt="مسكة عروس تيوليب بيضاء مع لولو على طاولة خشب — هدايا سلمى" width="843" height="1124" fetchpriority="high">
  </picture>
  <div class="hero-card">
    <span class="eyebrow">SALMA GIFTS</span>
    <h1>مسكات عرايس وصواني خطوبة وبكجات كتب الكتاب</h1>
    <p class="hero-sub">هدايا مناسبتكم بأسمائكم وتاريخ يومكم، بالتوصيل لكل محافظات الأردن</p>
    <div class="divider"><span></span></div>
    <ul class="promises">
      <li>معاينة عند الاستلام</li><li>الدفع عند الاستلام</li>
      <li>توصيل لكل المحافظات</li><li>جاهزة خلال يومين</li>
    </ul>
    <div class="price-pill"><strong>مسكة العروس</strong><b>{P['masaka']}</b><strong>دينار</strong><span>{withdel('masaka')} شامل التوصيل</span></div>
    {cta("للحجز راسلونا", "btn btn-outline", "cta_hero")}
    <div class="hero-links"><span dir="ltr">@salma.gifts1</span><span aria-hidden="true">·</span><a href="{MESSENGER}" target="_blank" rel="noopener">أو على ماسنجر</a></div>
  </div>
</section>

<!-- ===== المنتجات ===== -->
<section class="section"><div class="container">
  <div class="section-head"><h2>شو بتحبوا نجهزلكم؟</h2><a class="small" href="{PAGES['tawseel']['path']}">كل الأسعار ←</a></div>
  <div class="grid grid-cards">{card_html}</div>
</div></section>

<!-- ===== كيف أطلب ===== -->
<section class="section"><div class="container">
  <h2>كيف أطلب؟</h2>
  <ol class="grid grid-steps">{st}</ol>
  <p style="margin-top:16px">الموديل اللي ببالكم مش موجود؟ ابعتولنا صورته، ومنأكدلكم التوفر قبل الحجز.</p>
</div></section>

<!-- ===== من شغلنا ===== -->
<section class="section"><div class="container">
  <div class="section-head"><h2>من شغلنا</h2><a class="small" href="{IG}" target="_blank" rel="noopener">شوفوا أكثر على إنستغرام ←</a></div>
  <div class="grid grid-thumbs">{gal}</div>
</div></section>

<!-- ===== ليش هدايا سلمى ===== -->
<section class="section"><div class="container">
  <h2>ليش هدايا سلمى؟</h2>
  <div class="grid grid-info">
    <div class="info"><h3>أكثر من 600 طلب</h3><p>جهزنا مئات الصواني والمسكات والبكجات لعرايس من كل محافظات الأردن.</p></div>
    <div class="info"><h3>شوفوها قبل ما تدفعوا</h3><p>معاينة عند الاستلام، وإذا ما عجبتكم بترجعوها وبتدفعوا أجرة التوصيل بس.</p></div>
    <div class="info"><h3>بأسمائكم وتاريخكم</h3><p>الصواني والبكجات بتنعمل على الطلب بالأسماء والتاريخ والعبارة اللي بتختاروها.</p></div>
  </div>
</div></section>

<!-- ===== أسئلة ===== -->
<section class="section"><div class="container">
  <h2>أسئلة بتتكرر</h2>
  {faq_html(FAQ[:5])}
  <p style="margin-top:14px"><a href="{PAGES['faq']['path']}">كل الأسئلة ←</a></p>
</div></section>
"""
    title = "هدايا سلمى | مسكات عرايس وصواني خطوبة وبكجات كتب كتاب في الأردن"
    desc = f"مسكة عروس {P['masaka']} دينار، صينية خطوبة {P['saniya']} دينار، وبكجات كتب كتاب بأسمائكم. معاينة ودفع عند الاستلام وتوصيل لكل محافظات الأردن."
    write("/", layout("home", title, desc, body, [faq_schema(FAQ[:5])]))

# =====================================================================
# مسكات العرايس
# =====================================================================
def build_masakat():
    head, bsch = page_head("masakat", "مسكات عرايس في الأردن",
        f"مسكة العروس عنا بسعر <b>{P['masaka']} دينار</b>، و{withdel('masaka')} دينار مع التوصيل لأي محافظة. ورد صناعي عالي الجودة، من 20 لـ25 وردة، بموديلات وألوان متعددة تنفع لكتب الكتاب والخطوبة والعرس. وإذا حابين، منضيف عليها تعليقة بأسماء العروسين والتاريخ.")
    models = [("masaka-arous-1.webp", "مسكة ورد أبيض مع جبسوفيل"), ("masaka-arous-calla.webp", "مسكة كالا"),
              ("masaka-arous-trend.webp", "مسكة تيوليب مع لولو"), ("masaka-arous-pink.webp", "مسكة وردي وأبيض"),
              ("masaka-arous-2.webp", "مسكات كالا بقاعدة لولو"), ("masaka-arous-3.webp", "مسكة كالا طويلة"),
              ("masaka-arous-4.webp", "مسكة تيوليب مع طوق"), ("masaka-arous-tulip.webp", "مسكة تيوليب بقاعدة ستراس"),
              ("masaka-arous-5.webp", "مسكة تيوليب وكالا")]
    gal = "".join(f'<figure class="thumb">{img(i, a + " — مسكة عروس من هدايا سلمى")}<figcaption>{E(a)}</figcaption></figure>' for i, a in models)
    items = (product_card("مسكة العروس", "masaka", "masaka-arous-calla.webp", "مسكة عروس كالا بيضاء — هدايا سلمى",
                          "كل موديلات المسكات اللي بالصور بنفس السعر. ورد صناعي ما بيذبل، بيضل معكم ذكرى من يومكم.")
             + product_card("تعليقة للمسكة", "taliqa", "masaka-arous-4.webp", "مسكة عروس تيوليب مع تعليقة أكريليك — هدايا سلمى",
                            "تعليقة أكريليك عليها اسم العريس والعروس والتاريخ، بتنضاف على أي مسكة.",
                            note=f"إضافة · مسكة + تعليقة + توصيل = {P['masaka'] + P['taliqa'] + DELIVERY} دينار"))
    faqs = [FAQ[0], FAQ[1], FAQ[2], FAQ[7], FAQ[9]]
    body = head + f"""
<section class="section" style="padding-top:0"><div class="container">
  <div class="grid grid-cards">{items}</div>
</div></section>
<section class="section"><div class="container">
  <h2>موديلات المسكات</h2>
  <p>هدول من المسكات اللي بنجهزها. موديل عاجبكم مش هون؟ ابعتولنا صورته ومنأكدلكم التوفر قبل الحجز.</p>
  <div class="grid grid-thumbs">{gal}</div>
</div></section>
{info_boxes(["اختيار الموديل واللون من الصور", "تعليقة بأسماء العروسين والتاريخ (+" + str(P['taliqa']) + " دينار)", "ملاحظاتكم الخاصة على الطلب"])}
<section class="section"><div class="container">
  <h2>أسئلة عن مسكات العرايس</h2>
  {faq_html(faqs)}
  {related("masakat")}
</div></section>"""
    sch = [bsch, faq_schema(faqs),
           product_schema("مسكة العروس", "مسكة عروس من الورد الصناعي عالي الجودة، 20 إلى 25 وردة، بموديلات وألوان متعددة.",
                          ["masaka-arous-calla.webp", "masaka-arous-1.webp", "masaka-arous-trend.webp"], P["masaka"], sku="masaka")]
    write(PAGES["masakat"]["path"], layout("masakat",
        f"مسكة عروس في الأردن بسعر {P['masaka']} دينار | هدايا سلمى",
        f"مسكات عرايس من ورد صناعي عالي الجودة بموديلات متعددة، {P['masaka']} دينار و{withdel('masaka')} مع التوصيل لكل محافظات الأردن. معاينة ودفع عند الاستلام.",
        body, sch, og_img="masaka-arous-calla.webp"))

# =====================================================================
# صواني الخطوبة
# =====================================================================
def build_sawani():
    head, bsch = page_head("sawani", "صواني خطوبة ودبل بالأسماء",
        f"صينية الخطوبة أو الدبل بنجهزها مراية مزيّنة بأسماء العروسين وتاريخ المناسبة، مع آية أو عبارة من اختياركم. سعرها <b>{P['saniya']} دينار</b>، و{withdel('saniya')} مع التوصيل لكل محافظات الأردن.")
    items = product_card("صينية الخطوبة / الدبل", "saniya", "saniyet-khotoba-1.webp",
                         "صينية خطوبة مراية بالأسماء مع علب الدبل — هدايا سلمى",
                         "مراية بأسمائكم والتاريخ، مع علبتين للخواتم وشبر لولو ودانتيل بين الخواتم، وعليها طبقة حماية من الكسر.",
                         contents=["علبتين للخواتم", "أحرفكم على العلب مجاناً", "شبر لولو ودانتيل", "آية أو عبارة", "طبقة حماية من الكسر"])
    gal = "".join(f'<figure class="thumb">{img(i, a + " — هدايا سلمى")}<figcaption>{E(a)}</figcaption></figure>' for i, a in [
        ("saniyet-khotoba-1.webp", "صينية دبل مع ورد مجفف"), ("saniyet-khotoba-2.webp", "صينية دبل بالأحرف والتاريخ"),
        ("saniyet-khotoba-3.webp", "صينية دبل مع ورد ولولو"), ("bakj-berwaz-2.webp", "صينية دبل بإطار لولو")])
    faqs = [FAQ[3], FAQ[5], FAQ[6], FAQ[7], FAQ[9]]
    body = head + f"""
<section class="section" style="padding-top:0"><div class="container">
  <div class="grid grid-cards">{items}
    <div class="info"><h2>بدكم الصينية مع كتاب كتب الكتاب؟</h2>
      <p>وفّروا واطلبوها ضمن بكج: بكج البرواز بسعر {P['bakj_berwaz']} دينار، أو البكج الأساسي بسعر {P['bakj_asasi']} دينار مع كتاب عقد الزواج والبصمات ورسالة العمر.</p>
      <a class="btn btn-outline" href="{PAGES['bakjat']['path']}">شوفوا البكجات</a></div>
  </div>
</div></section>
<section class="section"><div class="container">
  <h2>موديلات الصواني</h2>
  <div class="grid grid-thumbs">{gal}</div>
</div></section>
<section class="section"><div class="container"><div class="grid grid-info">
  <div class="info"><h2>إضافات على الصينية</h2>
    <table class="prices"><tbody>
      <tr><td>ستاند أسود</td><td>+{P['stand']} دينار</td></tr>
      <tr><td>قصاصات</td><td>+{P['qassasat']} دنانير</td></tr>
      <tr><td>فناجين بالأسماء</td><td>+{P['fanajin']} دنانير</td></tr>
      <tr><td>قصاصة التقويم / رسالة العمر</td><td>+{P['taqweem']} دينار</td></tr>
    </tbody></table></div>
</div></div></section>
{info_boxes(["أسماء العروسين وتاريخ الخطوبة", "الآية موجودة، أو عبارة بدالها حسب طلبكم", "أحرفكم على علب الدبل مجاناً"])}
<section class="section"><div class="container">
  <h2>أسئلة عن صواني الخطوبة</h2>
  {faq_html(faqs)}
  {related("sawani")}
</div></section>"""
    sch = [bsch, faq_schema(faqs),
           product_schema("صينية الخطوبة والدبل", "صينية مراية بأسماء العروسين والتاريخ مع علبتين للخواتم ولولو ودانتيل وطبقة حماية من الكسر.",
                          ["saniyet-khotoba-1.webp", "saniyet-khotoba-2.webp", "saniyet-khotoba-3.webp"], P["saniya"], sku="saniya")]
    write(PAGES["sawani"]["path"], layout("sawani",
        f"صينية خطوبة ودبل بالأسماء بسعر {P['saniya']} دينار | هدايا سلمى",
        f"صواني خطوبة ودبل مراية بأسماء العروسين والتاريخ مع علب الخواتم. {P['saniya']} دينار و{withdel('saniya')} مع التوصيل لكل الأردن، معاينة ودفع عند الاستلام.",
        body, sch, og_img="saniyet-khotoba-1.webp"))

# =====================================================================
# البكجات
# =====================================================================
def build_bakjat():
    head, bsch = page_head("bakjat", "بكجات كتب الكتاب: شو بتشمل وكم سعرها",
        f"كل اللي بتحتاجوه لكتب الكتاب بطلب واحد، وبأسمائكم وتاريخ كتب الكتاب. عنا ثلاث بكجات: <b>بكج البرواز {P['bakj_berwaz']} دينار</b>، <b>البكج الأساسي {P['bakj_asasi']} دينار</b>، و<b>البكج الشامل {P['bakj_shamel']} دينار</b>، والتوصيل {DELIVERY} دينار لكل المحافظات.")
    items = (product_card("بكج البرواز", "bakj_berwaz", "bakj-berwaz-1.webp", "بكج البرواز: صينية دبل وبرواز بصمات بالأسماء — هدايا سلمى",
                          "صينية الدبل مع برواز للبصمات بدل الكتاب.", contents=["صينية الدبل", "علب الخواتم بالأحرف", "برواز بصمات بالأسماء", "حبر البصمات"])
             + product_card("البكج الأساسي", "bakj_asasi", "bakj-katb-ktab-2.webp", "البكج الأساسي: صينية دبل وكتاب عقد زواج وبصمات — هدايا سلمى",
                            "الأكثر طلباً لكتب الكتاب.", badge="الأكثر طلباً",
                            contents=["صينية الدبل", "علب الخواتم بالأحرف", "كتاب عقد الزواج والتوقيع والبصمات", "حبر البصمات", "رسالة العمر", "شبر لولو بين الخواتم"])
             + product_card("البكج الشامل", "bakj_shamel", "bakj-katb-ktab-1.webp", "البكج الشامل لكتب الكتاب — هدايا سلمى",
                            "البكج الأساسي كامل ومعه فناجين وقصاصات.", contents=["كل محتويات البكج الأساسي", "فناجين", "قصاصات"])
             + product_card("كتاب / دفتر توقيع لحاله", "kitab", "bakj-katb-ktab-1.webp", "كتاب عقد زواج وتوقيع وبصمات بالأسماء — هدايا سلمى",
                            "كتاب للتوقيع والبصمات بأسمائكم وتاريخ كتب الكتاب، إذا عندكم صينية أصلاً."))
    gal = "".join(f'<figure class="thumb">{img(i, a + " — هدايا سلمى")}<figcaption>{E(a)}</figcaption></figure>' for i, a in [
        ("bakj-katb-ktab-1.webp", "كتاب عقد الزواج بالأسماء"), ("bakj-katb-ktab-2.webp", "البكج الأساسي"),
        ("bakj-berwaz-1.webp", "بكج البرواز"), ("bakj-berwaz-3.webp", "برواز البصمات")])
    faqs = [FAQ[4], FAQ[5], FAQ[7], FAQ[8], FAQ[9]]
    body = head + f"""
<section class="section" style="padding-top:0"><div class="container">
  <div class="grid grid-cards">{items}</div>
</div></section>
<section class="section"><div class="container">
  <h2>من بكجات كتب الكتاب</h2>
  <div class="grid grid-thumbs">{gal}</div>
</div></section>
<section class="section"><div class="container">
  <h2>مقارنة سريعة</h2>
  <table class="prices"><thead><tr><th>البكج</th><th>السعر</th><th>مع التوصيل</th><th>شو بشمل</th></tr></thead><tbody>
    <tr><td>بكج البرواز</td><td>{P['bakj_berwaz']} دينار</td><td>{withdel('bakj_berwaz')} دينار</td><td>صينية + برواز بصمات + حبر</td></tr>
    <tr><td>البكج الأساسي</td><td>{P['bakj_asasi']} دينار</td><td>{withdel('bakj_asasi')} دينار</td><td>صينية + كتاب توقيع وبصمات + حبر + رسالة العمر</td></tr>
    <tr><td>البكج الشامل</td><td>{P['bakj_shamel']} دينار</td><td>{withdel('bakj_shamel')} دينار</td><td>الأساسي + فناجين + قصاصات</td></tr>
  </tbody></table>
</div></section>
{info_boxes(["أسماء العروسين وتاريخ كتب الكتاب", "الآية على الصينية، أو عبارة بدالها", "أحرفكم على علب الدبل مجاناً"])}
<section class="section"><div class="container">
  <h2>أسئلة عن بكجات كتب الكتاب</h2>
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
    head, bsch = page_head("mahr", "صندوق المهر: أجمل طريقة لتقديم المهر للعروس",
        f"صندوق فاخر لتقديم المهر للعروس، شامل كامل الزينة والإكسسوارات، بسعر <b>{P['mahr']} دينار</b> و{withdel('mahr')} مع التوصيل. الصندوق كميته محدودة، فاسألونا عن التوفر قبل الحجز.")
    items = product_card("صندوق المهر", "mahr", "sandouq-mahr-1.webp", "صندوق مهر خشبي فاخر لتقديم المهر للعروس — هدايا سلمى",
                         "شامل كامل الزينة والإكسسوارات. بنقدر نضيف أسماء العروسين أو عبارة.", badge="حسب التوفر، اسألونا")
    faqs = [("قديش سعر صندوق المهر؟", f"{P['mahr']} دينار، و{withdel('mahr')} مع التوصيل لكل محافظات الأردن. الكمية محدودة، فراسلونا نتأكد من التوفر."),
            FAQ[6], FAQ[8], FAQ[9]]
    body = head + f"""
<section class="section" style="padding-top:0"><div class="container">
  <div class="grid grid-cards">{items}
    <div class="info"><h2>فكرة حلوة للعريس وأهله</h2><p>بدل ما يتقدّم المهر بظرف، صندوق مرتب ومزيّن بيخلّي اللحظة أحلى بالصور، وبيضل ذكرى عند العروس.</p>
      <a class="btn btn-outline" href="{PAGES['bakjat']['path']}">شوفوا بكجات كتب الكتاب</a></div>
  </div>
</div></section>
{info_boxes(["أسماء العروسين على الصندوق", "عبارة من اختياركم"])}
<section class="section"><div class="container">
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
    head, bsch = page_head("grad", "هدايا تخرج بالاسم: صينية التخرج",
        f"صينية تخرج باسم الخريج أو الخريجة والتخصص، هدية مميزة للحفلة وللصور. سعرها <b>{P['takharroj']} دينار</b>، و{withdel('takharroj')} مع التوصيل لكل محافظات الأردن.")
    items = product_card("صينية التخرج", "takharroj", "hadiyet-takharroj-1.webp", "صينية تخرج باسم الخريجة والتخصص — هدايا سلمى",
                         "باسم الخريج أو الخريجة والتخصص، مع ورد وزينة. فيكم تضيفوا ستاند أسود.",
                         contents=["اسم الخريج/ة", "التخصص", f"ستاند أسود (+{P['stand']} دينار)"])
    faqs = [FAQ[12], FAQ[6], FAQ[7], FAQ[8], FAQ[9]]
    body = head + f"""
<section class="section" style="padding-top:0"><div class="container">
  <div class="grid grid-cards">{items}
    <div class="info"><h2>كيف تطلبوها</h2><p>ابعتولنا اسم الخريج أو الخريجة كما بدكم ينكتب، والتخصص، واسم المستلم ورقم الهاتف والمحافظة.</p>
      {cta("اطلبوها على إنستغرام", "btn btn-outline", "cta_grad")}</div>
  </div>
</div></section>
{info_boxes(["اسم الخريج أو الخريجة", "التخصص", f"ستاند أسود (+{P['stand']} دينار)"])}
<section class="section"><div class="container">
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
    head, bsch = page_head("tawseel", "الأسعار، التوصيل وطريقة الطلب",
        "ما في سلة ولا دفع أونلاين. كل الطلبات برسالة على إنستغرام أو ماسنجر، والدفع عند الاستلام بعد المعاينة.")
    rows = [("مسكة العروس", "masaka", PAGES["masakat"]["path"]), ("صينية الخطوبة / الدبل", "saniya", PAGES["sawani"]["path"]),
            ("بكج البرواز", "bakj_berwaz", PAGES["bakjat"]["path"]), ("البكج الأساسي", "bakj_asasi", PAGES["bakjat"]["path"]),
            ("البكج الشامل", "bakj_shamel", PAGES["bakjat"]["path"]), ("كتاب / دفتر توقيع لحاله", "kitab", PAGES["bakjat"]["path"]),
            ("صندوق المهر (حسب التوفر)", "mahr", PAGES["mahr"]["path"]), ("صينية التخرج", "takharroj", PAGES["grad"]["path"])]
    tr = "".join(f'<tr><td><a href="{u}">{E(n)}</a></td><td>{P[k]} دينار</td><td>{withdel(k)} دينار</td></tr>' for n, k, u in rows)
    adds = [("تعليقة للمسكة", "taliqa"), ("ستاند أسود", "stand"), ("قصاصات", "qassasat"), ("فناجين", "fanajin"), ("قصاصة التقويم / رسالة العمر", "taqweem")]
    ta = "".join(f"<tr><td>{E(n)}</td><td>+{P[k]} دينار</td></tr>" for n, k in adds)
    govs = "عمّان، الزرقاء، إربد، السلط (البلقاء)، مأدبا، جرش، عجلون، المفرق، الكرك، الطفيلة، معان، العقبة"
    body = head + f"""
<section class="section" style="padding-top:0"><div class="container">
  <h2>كل الأسعار</h2>
  <table class="prices"><thead><tr><th>المنتج</th><th>السعر</th><th>مع التوصيل</th></tr></thead><tbody>{tr}</tbody></table>
  <h3 style="margin-top:24px">الإضافات</h3>
  <table class="prices"><tbody>{ta}<tr><td>أحرفكم على علب الدبل</td><td>مجاناً</td></tr></tbody></table>
</div></section>
<section class="section"><div class="container"><div class="grid grid-info">
  <div class="info"><h2>التوصيل</h2><ul>
    <li>لكل محافظات الأردن: {govs}.</li>
    <li>أجرة التوصيل {DELIVERY} دينار لأي محافظة.</li>
    <li>الطلب بيجهز وبيوصل خلال يومين كحد أقصى.</li>
  </ul></div>
  <div class="info"><h2>الحجز والدفع</h2><ul>
    <li>الحجز قبل المناسبة بثلاثة أيام على الأقل.</li>
    <li>الدفع عند الاستلام: كاش أو كليك مع المندوب.</li>
    <li>معاينة عند الاستلام. إذا ما عجبكم الطلب بترجعوه وبتدفعوا أجرة التوصيل بس.</li>
  </ul></div>
  <div class="info"><h2>شو تبعتولنا بالرسالة</h2><ul>
    <li>المنتج والموديل (أو صورة الموديل).</li>
    <li>أسماء العروسين والتاريخ (أو اسم الخريج/ة والتخصص).</li>
    <li>اسم المستلم ورقم الهاتف.</li>
    <li>المحافظة والمنطقة، واليوم المناسب للاستلام.</li>
  </ul>{cta("ابعتوا رسالة على إنستغرام", "btn btn-gold", "cta_order")}</div>
</div></div></section>
<section class="section"><div class="container">
  {related("tawseel")}
</div></section>"""
    sch = [bsch]
    write(PAGES["tawseel"]["path"], layout("tawseel",
        "الأسعار والتوصيل وطريقة الطلب | هدايا سلمى",
        f"أسعار مسكات العرايس وصواني الخطوبة والبكجات، والتوصيل لكل محافظات الأردن بسعر {DELIVERY} دينار خلال يومين. دفع ومعاينة عند الاستلام.",
        body, sch))

# =====================================================================
# الأسئلة الشائعة
# =====================================================================
def build_faq():
    head, bsch = page_head("faq", "أسئلة شائعة عن هدايا سلمى",
        "أكثر الأسئلة اللي بتوصلنا عن المسكات والصواني والبكجات والأسعار والتوصيل. سؤالكم مش هون؟ راسلونا على إنستغرام.")
    body = head + f"""
<section class="section" style="padding-top:0"><div class="container">
  {faq_html(FAQ)}
  {related("faq")}
</div></section>"""
    write(PAGES["faq"]["path"], layout("faq",
        "أسئلة شائعة: أسعار المسكات والصواني والتوصيل | هدايا سلمى",
        f"من وين أشتري مسكة عروس بالأردن؟ قديش سعر صينية الخطوبة؟ بتوصلوا لكل المحافظات؟ كل الأجوبة عن هدايا سلمى بمكان واحد.",
        body, [bsch, faq_schema(FAQ)]))

# =====================================================================
# 404
# =====================================================================
def build_404():
    body = f"""<section class="section"><div class="container" style="text-align:center;padding:40px 16px">
  <h1>الصفحة مش موجودة</h1>
  <p>يمكن الرابط تغيّر. جرّبوا من هون:</p>
  <p><a class="btn btn-gold" href="/">الرئيسية</a></p>
  {related(None)}
</div></section>"""
    PAGES["404"] = {"path": "/404.html", "nav": "404"}
    out = layout("404", "الصفحة مش موجودة | هدايا سلمى", "الصفحة المطلوبة غير موجودة.", body, [])
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
        f"- كتاب / دفتر توقيع لحاله: {P['kitab']}",
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
