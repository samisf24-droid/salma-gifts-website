# -*- coding: utf-8 -*-
"""
مولّد صفحات موقع هدايا سلمى.

كل الأسعار والنصوص الأساسية موجودة بأعلى هاد الملف (PRICES و STYLES و FAQ).
بعد أي تعديل:  python3 _build/build.py
بيعيد كتابة كل صفحات الـHTML و sitemap.xml و llms.txt بالأسعار الجديدة.
(إذا عدّلت HTML يدوياً بدون هاد السكربت، تعديلك بينمسح عند التشغيل الجاي —
 فالأفضل دايماً تعدّل هون.)
"""
import json, os, html, datetime, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://salmagifts.com"
IG_DM = "https://ig.me/m/salma.gifts1"
IG = "https://www.instagram.com/salma.gifts1/"
FB = "https://www.facebook.com/101132472391425"
MESSENGER = "https://m.me/101132472391425"
DELIVERY = 2
TODAY = datetime.date.today().isoformat()
VERSION = "5"  # غيّره لما تعدّل style.css أو main.js عشان المتصفحات تجيب النسخة الجديدة
SLOGAN = "لتبقى ذكرياتكم الجميلة، خالدة."

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
# الصفحات — لا تغيّر أي رابط موجود (بنخسر ترتيب جوجل)
# =====================================================================
PAGES = {
    "home":  {"path": "/", "nav": "الرئيسية"},
    "masakat": {"path": "/masakat-arayes/", "nav": "مسكات العروس"},
    "sawani": {"path": "/sawani-khotoba/", "nav": "صواني الخطوبة"},
    "bakjat": {"path": "/bakjat-katb-ktab/", "nav": "بكجات كتب الكتاب"},
    "mahr": {"path": "/sandouq-mahr/", "nav": "صندوق المهر"},
    "grad": {"path": "/hadaya-takharroj/", "nav": "هدايا التخرج"},
    "tawseel": {"path": "/tawseel/", "nav": "الأسعار والتوصيل"},
    "faq": {"path": "/as2ila/", "nav": "أسئلة شائعة"},
}
NAV_ORDER = ["masakat", "sawani", "bakjat", "mahr", "grad", "tawseel", "faq"]

# =====================================================================
# أنواع المسكات — كل نوع إله صفحة (إلا البيوني: قسم بصفحة المسكات)
# الأسماء هي نفس الكلمات اللي الناس بتبحث فيها بالأردن.
# =====================================================================
STYLES = [
    {"key": "tulip", "path": "/masakat-arayes/tulip/", "name": "توليب", "nav": "مسكة عروس توليب",
     "h1": "مسكة عروس توليب",
     "lead": "التوليب الأبيض أكثر ما تطلبه العرائس عندنا: ناعم وأنيق، ويليق بالخطوبة وعقد القران والزفاف.",
     "about": ["نجهّز مسكة التوليب بثلاث طرق: توليب مع لولو، أو توليب مع جبسوفيل (بيبي بريث)، أو توليب بحبّات الكريستال. وكلها بالسعر نفسه.",
               "الورد صناعي عالي الجودة فلا يذبل، وتبقى المسكة ذكرى في بيتكم بعد المناسبة. ويمكن إضافة تعليقة بأسمائكم وتاريخ المناسبة."],
     "photos": [("masaka-arous-tulip.webp", "مسكة عروس توليب أبيض بقاعدة ستراس ولولو", "توليب بقاعدة ستراس"),
                ("masaka-arous-trend.webp", "مسكة عروس توليب مع لولو", "توليب مع لولو"),
                ("masaka-arous-4.webp", "مسكة عروس توليب مع تعليقة أكريليك بالأسماء", "توليب مع تعليقة بالأسماء")],
     "faq": [("كم سعر مسكة العروس التوليب؟", None), ("هل التوليب طبيعي؟", "لا، توليب صناعي عالي الجودة يشبه الطبيعي ولا يذبل، فيبقى بحالته بعد المناسبة.")]},
    {"key": "crystal", "path": "/masakat-arayes/crystal/", "name": "كريستال", "nav": "مسكة عروس كريستال",
     "h1": "مسكة عروس كريستال",
     "lead": "توليب أبيض تحيطه حبّات كريستال ولولو، تلمع مع كل حركة. لمن تريد مسكة فخمة دون مبالغة.",
     "about": ["تُلفّ المسكة بتل شفاف ناعم، وتتوزّع حبّات الكريستال واللولو بين الورد بتنسيق متناسق. ويمكن اختيار كمية الكريستال وتوزيعه حسب رغبتكم.",
               "مثل باقي مسكاتنا، تُجهَّز كل واحدة على حدة وتصلكم خلال يومين، وتعاينونها قبل الدفع."],
     "photos": [("masaka-arous-crystal.webp", "مسكة عروس توليب بالكريستال", "توليب بالكريستال"),
                ("masaka-arous-crystal-2.webp", "مسكة عروس توليب بحبات الكريستال على السيقان", "حبّات الكريستال على السيقان"),
                ("masaka-arous-crystal-detail.webp", "تفاصيل مسكة عروس بالكريستال واللولو والتل", "كريستال ولولو وتل")],
     "faq": [("كم سعر مسكة العروس الكريستال؟", None), ("هل يمكن زيادة الكريستال؟", "نعم، أخبرونا عند الطلب بالكمية والتوزيع الذي تفضّلونه، ونجهّزها على هذا الأساس.")]},
    {"key": "calla", "path": "/masakat-arayes/calla/", "name": "كالا", "nav": "مسكة عروس كالا",
     "h1": "مسكة عروس كالا",
     "lead": "زهر الكالا الأبيض بخطوطه الطويلة يعطي المسكة أناقة ملكية، وحده أو مع الجوري الملوّن.",
     "about": ["نجهّز الكالا بقاعدة من اللولو أو الستراس، أو نمزجه مع الجوري الأزرق أو بلون يناسب فستانكم.",
               "والكالا صناعي عالي الجودة لا يذبل، فيمكن الاحتفاظ بالمسكة بعد المناسبة."],
     "photos": [("masaka-arous-calla.webp", "مسكة عروس كالا بيضاء مع لولو", "كالا أبيض مع لولو"),
                ("masaka-arous-calla-blue.webp", "مسكة عروس كالا مع جوري أزرق وجبسوفيل", "كالا مع جوري أزرق"),
                ("masaka-arous-3.webp", "مسكة عروس كالا طويلة بقاعدة ستراس", "كالا طويلة"),
                ("masaka-arous-2.webp", "مسكات عروس كالا بقاعدة لولو", "كالا بقاعدة لولو")],
     "faq": [("كم سعر مسكة العروس الكالا؟", None), ("هل يمكن مزج الكالا مع ورد ملوّن؟", "نعم، مثل الكالا مع الجوري الأزرق، أو بأي لون يناسب فستانكم.")]},
    {"key": "jouri", "path": "/masakat-arayes/jouri/", "name": "جوري", "nav": "مسكة عروس جوري",
     "h1": "مسكة عروس جوري",
     "lead": "الجوري مع الجبسوفيل: رقّة وأنوثة، بالأبيض أو بلون تختارونه.",
     "about": ["نجهّز مسكة الجوري بالأبيض الكلاسيكي مع الجبسوفيل، أو بالأزرق مع الكالا، أو بلون يناسب فستانكم.",
               "تُلفّ القاعدة بالستراس أو التل أو اللولو حسب رغبتكم، وتُجهَّز كل مسكة على حدة."],
     "photos": [("masaka-arous-jouri.webp", "مسكات عروس جوري أبيض مع جبسوفيل", "جوري مع جبسوفيل"),
                ("masaka-arous-calla-blue.webp", "مسكة عروس جوري أزرق مع كالا", "جوري أزرق مع كالا")],
     "faq": [("كم سعر مسكة العروس الجوري؟", None), ("هل يتوفر الجوري بألوان؟", "نعم، الأبيض هو الأكثر طلبًا، ونجهّز الأزرق والوردي وأي لون يناسب فستانكم.")]},
]
PEONY = ("masaka-arous-1.webp", "مسكة عروس بيوني أبيض مع جبسوفيل", "بيوني أبيض مع جبسوفيل")

# =====================================================================
# الأسئلة الشائعة — نفس صيغة سؤال الناس
# =====================================================================
FAQ = [
    ("من أين أشتري مسكة عروس في الأردن؟",
     f"من هدايا سلمى، حيث نجهّز مسكات العرائس من التوليب والكريستال والكالا والجوري والبيوني بسعر {P['masaka']} دينارًا، ونوصلها إلى جميع محافظات الأردن مقابل {DELIVERY} دينار. يتم الطلب برسالة على إنستغرام salma.gifts1."),
    ("كم سعر مسكة العروس؟",
     f"سعرها {P['masaka']} دينارًا لجميع الأنواع، و{withdel('masaka')} دينارًا شاملة التوصيل. ويمكن إضافة تعليقة تحمل اسمَي العروسين والتاريخ مقابل {P['taliqa']} دينار."),
    ("هل ورد المسكة طبيعي أم صناعي؟",
     "ورد صناعي عالي الجودة لا يذبل، فتبقى المسكة ذكرى دائمة. وتضم كل مسكة ما بين 20 و25 وردة."),
    ("كم سعر صينية الخطوبة؟",
     f"سعرها {P['saniya']} دينارًا، و{withdel('saniya')} دينارًا شاملة التوصيل. وهي مرآة بأسمائكم بظهر خشبي يحميها من الكسر، مع علبتين للخواتم تحملان حرفيكم الأولين مجانًا، وشريط من اللؤلؤ والدانتيل."),
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
    ("ما أنواع مسكات العروس لديكم؟",
     "توليب (مع لولو أو جبسوفيل أو كريستال)، وكريستال، وكالا، وجوري، وبيوني، وألوان حسب الطلب. وإن أعجبكم تصميم غير موجود، أرسلوا لنا صورته."),
    ("هل يمكن أن يكون لون المسكة مثل لون الفستان؟",
     "نعم، نجهّز المسكة باللون الذي يناسب فستانكم، للخطوبة أو الحنّة أو عقد القران أو الزفاف أو التخرج."),
]
FAQ_BY_Q = {q: a for q, a in FAQ}

# =====================================================================
# أدوات صغيرة
# =====================================================================
E = html.escape

# تمديد الأسماء بالكشيدة — نفس قاعدة شهادات القِران (وبنفسها بالـJS)
CONNECT_AFTER = set("بتثجحخسشصضطظعغفقكلمنهيئ")
def kashida(name):
    def word(w):
        w = w.replace("ـ", "")
        letters = re.sub(r"[ً-ْ]", "", w)
        if len(letters) < 2:
            return w
        n = 4 if len(letters) >= 4 else 3
        for i in range(len(w) - 2, -1, -1):
            if w[i] in CONNECT_AFTER and "ء" < w[i + 1] <= "ي" and w[i + 1] != "ء":
                return w[:i + 1] + "ـ" * n + w[i + 1:]
        return w
    return " ".join(word(x) for x in name.split())

def img(src, alt, cls="", lazy=True, w=720, h=900):
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/{src}" alt="{E(alt)}" width="{w}" height="{h}"'
            + (' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"') + '>')

IG_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".9" fill="currentColor" stroke="none"/></svg>'
ARROW = '<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg>'
DIAMOND = '<div class="divider" aria-hidden="true"><span></span></div>'

def cta(label="راسلونا للحجز", cls="btn btn-primary", event="cta"):
    return f'<a class="{cls}" href="{IG_DM}" target="_blank" rel="noopener" data-event="{event}">{IG_ICON}<span>{label}</span></a>'

def faq_html(items):
    out = ['<div class="faq">']
    for q, a in items:
        out.append(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>')
    out.append('</div>')
    return "\n".join(out)

def faq_schema(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

def breadcrumb(trail):
    """trail: [(name, path), ...] بدون الرئيسية؛ آخر عنصر هو الصفحة الحالية."""
    items = [("الرئيسية", "/")] + trail
    lis = "".join(
        (f'<li aria-current="page">{E(n)}</li>' if i == len(items) - 1 else f'<li><a href="{p}">{E(n)}</a></li>')
        for i, (n, p) in enumerate(items))
    h = f'<nav class="breadcrumb container" aria-label="مسار الصفحة"><ol>{lis}</ol></nav>'
    sch = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(items)]}
    return h, sch

def bc_page(key):
    return breadcrumb([(PAGES[key]["nav"], PAGES[key]["path"])])

STORE_ID = SITE + "/#store"
STORE = {
    "@type": "OnlineStore", "@id": STORE_ID,
    "name": "Salma Gifts - هدايا سلمى", "alternateName": ["هدايا سلمى", "Salma Gifts", "سلمى للهدايا"],
    "url": SITE + "/", "logo": SITE + "/assets/img/logo-512.png",
    "image": SITE + "/assets/img/og-salma-gifts.jpg",
    "slogan": SLOGAN,
    "description": "متجر أردني أونلاين لهدايا المناسبات حسب الطلب: مسكات العروس (توليب، كريستال، كالا، جوري، بيوني)، صواني الخطوبة والدبل من المرآة بالأسماء، بكجات كتب الكتاب، صندوق المهر وهدايا التخرج، بالتوصيل لكل محافظات الأردن.",
    "areaServed": {"@type": "Country", "name": "Jordan"},
    "address": {"@type": "PostalAddress", "addressCountry": "JO"},
    "currenciesAccepted": "JOD", "paymentAccepted": "Cash, CliQ",
    "knowsAbout": ["مسكة عروس", "مسكات عروس", "مسكة عروس توليب", "مسكة عروس كريستال", "مسكة عروس كالا",
                   "صينية خطوبة", "صينية دبل الخطوبة", "بكج كتب الكتاب", "صندوق المهر", "هدايا تخرج"],
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
def layout(key, path, title, desc, body, schemas, og_img="og-salma-gifts.jpg"):
    canonical = SITE + path
    nav_key = key if key in PAGES else ("masakat" if key.startswith("style") else None)
    nav = "".join(
        f'<a href="{PAGES[k]["path"]}"' + (' aria-current="page"' if k == nav_key else "") + f'>{E(PAGES[k]["nav"])}</a>'
        for k in NAV_ORDER)
    mnav = '<a href="/"' + (' aria-current="page"' if key == "home" else "") + '>الرئيسية</a>' + nav
    graph = [STORE, {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/",
                     "name": "هدايا سلمى - Salma Gifts", "inLanguage": "ar", "publisher": {"@id": STORE_ID}}]
    graph += [s for s in schemas if s]
    for g in graph:
        if g.get("@type") == "Product":
            g["offers"]["url"] = canonical
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    extra_preload = '\n<link rel="preload" href="/assets/fonts/amiri-700-arabic.woff2" as="font" type="font/woff2" crossorigin>' if key == "home" else ""
    robots = '<meta name="robots" content="noindex">' if key == "404" else '<meta name="robots" content="index, follow, max-image-preview:large">'
    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
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
<link rel="preload" href="/assets/fonts/aref-ruqaa-700-arabic.woff2" as="font" type="font/woff2" crossorigin>{extra_preload}
<link rel="stylesheet" href="/assets/css/style.css?v={VERSION}">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<a class="skip" href="#main">تخطَّ إلى المحتوى</a>

<header class="site-header">
  <div class="header-row">
    <a class="brand" href="/" aria-label="هدايا سلمى - الرئيسية">
      <img src="/assets/img/logo.webp" alt="شعار هدايا سلمى Salma Gifts" width="40" height="42">
      <span class="brand-name">هدايا سلمى</span>
    </a>
    <nav class="main-nav" aria-label="القائمة الرئيسية">{nav}</nav>
    {cta("احجزوا الآن", "btn btn-primary btn-sm header-cta", "cta_header")}
    <button class="menu-btn" type="button" aria-label="القائمة" aria-expanded="false" aria-controls="mobile-nav">
      <span></span><span></span>
    </button>
  </div>
  <nav class="mobile-nav" id="mobile-nav" aria-label="القائمة">{mnav}</nav>
</header>

<main id="main">
{body}
</main>

<section class="closing">
  <div class="container">
    {DIAMOND}
    <p class="closing-title">هل اقترب موعد مناسبتكم؟</p>
    <p>أرسلوا لنا الأسماء والتاريخ، ونجهّز طلبكم خلال يومين.</p>
    {cta("تواصلوا معنا على إنستغرام", "btn btn-primary", "cta_closing")}
  </div>
</section>

<footer class="site-footer">
  <div class="footer-grid container">
    <div>
      <p class="footer-brand">هدايا سلمى</p>
      <p class="footer-slogan">{SLOGAN}</p>
      <p>هدايا الخطوبة وعقد القران والتخرج، تُجهَّز حسب الطلب في الأردن وتُوصَل إلى جميع المحافظات.</p>
    </div>
    <ul>
      {"".join(f'<li><a href="{PAGES[k]["path"]}">{E(PAGES[k]["nav"])}</a></li>' for k in NAV_ORDER)}
    </ul>
    <ul>
      {"".join(f'<li><a href="{s["path"]}">{E(s["nav"])}</a></li>' for s in STYLES)}
      <li><a href="{IG}" target="_blank" rel="noopener">إنستغرام: salma.gifts1</a></li>
      <li><a href="{FB}" target="_blank" rel="noopener">فيسبوك</a> · <a href="{MESSENGER}" target="_blank" rel="noopener">ماسنجر</a></li>
    </ul>
  </div>
  <p class="copy">© {datetime.date.today().year} Salma Gifts - هدايا سلمى، الأردن</p>
</footer>

<div class="sticky-cta">{cta("احجزوا عبر إنستغرام", "btn btn-primary btn-block", "cta_sticky")}</div>
<div class="toast" role="status" aria-live="polite"></div>
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

def mosaic(items, eager_first=True):
    """صورة كبيرة وصور أصغر جنبها — بدل صف صور متساوية."""
    figs = "".join(
        f'<figure>{img(i, a, lazy=not (eager_first and n == 0))}<figcaption>{E(c)}</figcaption></figure>'
        for n, (i, a, c) in enumerate(items))
    return f'<div class="mosaic n{len(items)}">{figs}</div>'

def section(title, inner, cls="", intro=""):
    i = f'<p class="section-intro">{intro}</p>' if intro else ""
    return f"""<section class="section {cls}"><div class="container">
  <h2>{E(title)}</h2>{i}
  {inner}
</div></section>"""

def includes(items):
    return '<ul class="includes">' + "".join(f"<li>{E(x)}</li>" for x in items) + "</ul>"

def price_line(k, note=None):
    note = note or f"{withdel(k)} دينارًا شاملة التوصيل إلى أي محافظة"
    return f'<p class="p-price"><b>{P[k]} <small>دينار</small></b><span>{E(note)}</span></p>'

def page_intro(trail, h1, lead, k=None, note=None, extra=""):
    """رأس صفحة المنتج: العنوان والسعر والزر — الصور تحته مباشرة."""
    bc, sch = breadcrumb(trail)
    pr = price_line(k, note) if k else ""
    return bc + f"""
<section class="p-head container">
  <h1>{E(h1)}</h1>
  <p class="lead">{lead}</p>
  {pr}{extra}
  <div class="actions">{cta("احجزوا الآن", "btn btn-primary", "cta_product")}</div>
</section>""", sch

# =====================================================================
# معاينة الأسماء على الصينية — قلب الصفحة الرئيسية
# =====================================================================
def name_preview():
    g, b = "سيف", "نور"
    return f"""
<section class="hero">
  <div class="container hero-inner">
    <h1>مسكات عروس وصواني خطوبة <span>بأسمائكم</span></h1>
    <p class="slogan">{SLOGAN}</p>

    <form class="maker" id="maker" action="{IG_DM}" target="_blank" novalidate>
      <div class="stage" data-mode="tray">
        <div class="tray" aria-hidden="true">
          <svg class="pearls" viewBox="0 0 200 200"><circle cx="100" cy="100" r="95.5"/><circle class="pearl-shine" cx="100" cy="100" r="95.5"/></svg>
          <div class="mirror">
            <p class="verse">وَجَعَلَ بَيْنَكُم مَّوَدَّةً وَرَحْمَةً</p>
            <div class="boxes"><span data-out="gi">{g[0]}</span><span data-out="bi">{b[0]}</span></div>
            <p class="names"><span data-out="g">{kashida(g)}</span><span class="amp">&amp;</span><span data-out="b">{kashida(b)}</span></p>
            <p class="date" data-out="d">12.12.2026</p>
          </div>
        </div>
        <div class="tag-scene" aria-hidden="true">
          {img("masaka-arous-tulip.webp", "", w=720, h=900)}
          <div class="tag">
            <p class="names"><span data-out="g">{kashida(g)}</span><span class="amp">&amp;</span><span data-out="b">{kashida(b)}</span></p>
            <p class="date" data-out="d">12.12.2026</p>
          </div>
        </div>
      </div>

      <div class="fields">
        <label class="field"><span>اسم العريس</span><input name="groom" autocomplete="off" maxlength="16" placeholder="{g}" inputmode="text"></label>
        <label class="field"><span>اسم العروس</span><input name="bride" autocomplete="off" maxlength="16" placeholder="{b}" inputmode="text"></label>
      </div>

      <fieldset class="choice">
        <legend class="sr">ماذا تريدون بهذه الأسماء؟</legend>
        <label><input type="radio" name="item" value="tray" checked data-price="{P['saniya']}" data-label="صينية خطوبة بالأسماء"><span>صينية خطوبة <b>{P['saniya']} دينار</b></span></label>
        <label><input type="radio" name="item" value="tag" data-price="{P['masaka'] + P['taliqa']}" data-label="مسكة عروس مع تعليقة بالأسماء"><span>مسكة مع تعليقة <b>{P['masaka'] + P['taliqa']} دينار</b></span></label>
      </fieldset>

      <button class="btn btn-primary btn-lg" type="submit" data-event="cta_maker">{IG_ICON}<span>احجزوا بهذه الأسماء</span></button>
      <details class="date-more">
        <summary>أضيفوا تاريخ المناسبة</summary>
        <label class="field field-date"><span>التاريخ <i>(اختياري)</i></span><input name="date" inputmode="numeric" autocomplete="off" maxlength="10" placeholder="12.12.2026" dir="ltr"></label>
      </details>
      <p class="maker-note">ننسخ لكم التفاصيل، وتُلصق في رسالة إنستغرام. معاينة تقريبية؛ يُكتب الاسم بخط يدوي على القطعة.</p>
    </form>
  </div>
</section>"""

# =====================================================================
# الرئيسية
# =====================================================================
def style_rail():
    items = [(s["path"], s["name"], s["photos"][0][0], s["photos"][0][1]) for s in STYLES]
    items.append((PAGES["masakat"]["path"] + "#peony", "بيوني", PEONY[0], PEONY[1]))
    lis = "".join(f"""<li><a href="{p}">{img(i, a, w=720, h=900)}<span class="label"><b>{E(n)}</b><span>{P['masaka']} دينار</span></span></a></li>"""
                  for p, n, i, a in items)
    return f'<ul class="rail">{lis}</ul>'

def menu_list(rows):
    """قائمة أسعار مثل منيو البوتيك: صورة صغيرة، الاسم، سطر، السعر."""
    out = []
    for href, name, line, k, im in rows:
        out.append(f"""<li><a href="{href}">
  {img(im, name + " من هدايا سلمى", w=720, h=900)}
  <span class="m-text"><b>{E(name)}</b><span>{E(line)}</span></span>
  <span class="m-price">{P[k]}<small>دينار</small></span>
</a></li>""")
    return '<ul class="menu">' + "".join(out) + "</ul>"

def build_home():
    rows = [
        (PAGES["sawani"]["path"], "صينية الخطوبة والدبل", "مرآة بأسمائكم بظهر خشبي، مع علب الخواتم", "saniya", "saniyet-khotoba-1.webp"),
        (PAGES["masakat"]["path"], "مسكة العروس", "توليب، كريستال، كالا، جوري، بيوني", "masaka", "masaka-arous-crystal.webp"),
        (PAGES["bakjat"]["path"], "البكج الأساسي لكتب الكتاب", "صينية وكتاب توقيع وبصمات ورسالة العمر", "bakj_asasi", "bakj-katb-ktab-2.webp"),
        (PAGES["bakjat"]["path"], "بكج البرواز", "صينية وبرواز بصمات بالأسماء", "bakj_berwaz", "bakj-berwaz-1.webp"),
        (PAGES["bakjat"]["path"], "البكج الشامل", "الأساسي مع الفناجين والقصاصات", "bakj_shamel", "bakj-berwaz-3.webp"),
        (PAGES["bakjat"]["path"], "كتاب التوقيع والبصمات", "بالأسماء وتاريخ كتب الكتاب، وحده", "kitab", "bakj-katb-ktab-1.webp"),
        (PAGES["mahr"]["path"], "صندوق المهر", "لتقديم المهر للعروس، حسب التوفر", "mahr", "sandouq-mahr-1.webp"),
        (PAGES["grad"]["path"], "صينية التخرج", "باسم الخريج أو الخريجة والتخصص", "takharroj", "hadiyet-takharroj-1.webp"),
    ]
    steps = [("اكتبوا الأسماء", "واختاروا التصميم من الموقع أو من إنستغرام."),
             ("أرسلوا الرسالة", "مع العنوان ورقم الهاتف."),
             ("استلموا وعاينوا", "خلال يومين، وادفعوا عند الاستلام.")]
    st = "".join(f'<li><b>{t}</b><span>{d}</span></li>' for t, d in steps)
    faqs = [FAQ[0], FAQ[1], FAQ[3], FAQ[9]]
    body = name_preview() + f"""
<section class="section styles" id="masakat"><div class="container">
  <div class="section-head"><h2>مسكة العروس، بالشكل الذي تحبينه</h2><a href="{PAGES['masakat']['path']}">كل المسكات {ARROW}</a></div>
  <p class="section-intro">ورد صناعي لا يذبل، من 20 إلى 25 وردة. كل الأنواع بسعر واحد: {P['masaka']} دينارًا.</p>
  {style_rail()}
</div></section>

<section class="section"><div class="container narrow-wide">
  <div class="section-head"><h2>كل ما نجهّزه</h2><a href="{PAGES['tawseel']['path']}">الأسعار والتوصيل {ARROW}</a></div>
  {menu_list(rows)}
</div></section>

<section class="section story"><div class="container story-inner">
  {img("masaka-arous-crystal-detail.webp", "تفاصيل مسكة عروس بالكريستال واللولو من تجهيز هدايا سلمى")}
  <div>
    <h2>كل قطعة تُجهَّز على حدة</h2>
    <p>لا نعمل بالجملة. كل مسكة وكل صينية تُجهَّز في ورشتنا بأسمائكم وتاريخ مناسبتكم، ونراجعها قبل أن تخرج إليكم.</p>
    <p>أنجزنا أكثر من <b>1500</b> طلب، ونجهّز أكثر من <b>120</b> طلبًا كل أسبوع، ولا يزال كل طلب يُعامل كأنه الوحيد. هدفنا أفضل جودة بأفضل سعر.</p>
    {promise_list()}
  </div>
</div></section>

<section class="section"><div class="container">
  <h2>كيف تطلبون</h2>
  <ol class="steps">{st}</ol>
</div></section>

<section class="section"><div class="container narrow">
  <div class="section-head"><h2>أسئلة متكررة</h2><a href="{PAGES['faq']['path']}">كل الأسئلة {ARROW}</a></div>
  {faq_html(faqs)}
</div></section>
"""
    title = "مسكة عروس وصينية خطوبة بالأسماء في الأردن | هدايا سلمى"
    desc = f"مسكة عروس {P['masaka']} دينار (توليب، كريستال، كالا، جوري، بيوني)، صينية خطوبة مرآة بالأسماء {P['saniya']} دينار، وبكجات كتب كتاب. معاينة ودفع عند الاستلام وتوصيل لكل محافظات الأردن."
    write("/", layout("home", "/", title, desc, body, [faq_schema(faqs)]))

# =====================================================================
# مسكات العروس (الصفحة الرئيسية للمسكات)
# =====================================================================
def build_masakat():
    head, bsch = page_intro([(PAGES["masakat"]["nav"], PAGES["masakat"]["path"])],
        "مسكة عروس في الأردن",
        "مسكات عروس من ورد صناعي عالي الجودة لا يذبل، من 20 إلى 25 وردة: توليب، كريستال، كالا، جوري وبيوني، وبأي لون يناسب فستانكم.",
        "masaka")
    cards = "".join(f"""<li><a href="{s['path']}">{img(s['photos'][0][0], s['photos'][0][1])}<span class="label"><b>{E(s['nav'])}</b><span>{P['masaka']} دينار</span></span></a></li>""" for s in STYLES)
    faqs = [FAQ[0], FAQ[1], FAQ[13], FAQ[14], FAQ[2], FAQ[7], FAQ[9]]
    body = head + f"""
<section class="section"><div class="container">
  <h2>أنواع مسكات العروس</h2>
  <p class="section-intro">كل الأنواع بسعر واحد. وإن أعجبكم تصميم غير موجود هنا، أرسلوا لنا صورته.</p>
  <ul class="rail rail-grid">{cards}</ul>
</div></section>

<section class="section" id="peony"><div class="container split">
  <div>
    <h2>مسكة عروس بيوني</h2>
    <p>ورد البيوني الأبيض بأوراقه الكثيفة مع الجبسوفيل، لمسكة ناعمة ممتلئة. ويتوفر بالوردي أو بلون حسب الطلب.</p>
    {price_line("masaka")}
  </div>
  <figure class="photo">{img(*PEONY[:2])}</figure>
</div></section>

<section class="section tint"><div class="container split">
  <div>
    <h2>باللون الذي يناسب فستانك</h2>
    <p>للخطوبة، أو الحنّة، أو عقد القران، أو الزفاف، أو التخرج. أرسلوا لنا لون الفستان ونجهّز المسكة على أساسه.</p>
  </div>
  <figure class="photo">{img("masaka-arous-pink-soft.webp", "مسكة عروس بألوان ناعمة وردية حسب الطلب")}</figure>
</div></section>

<section class="section"><div class="container split">
  <div>
    <h2>تعليقة بأسمائكم</h2>
    <p>يمكن إضافة تعليقة من الأكريليك إلى المسكة، تحمل اسمَي العريس والعروس وتاريخ المناسبة.</p>
    <p class="p-price"><b>+{P['taliqa']} <small>دينار</small></b><span>المسكة مع التعليقة والتوصيل: {P['masaka'] + P['taliqa'] + DELIVERY} دينارًا</span></p>
    <p><a class="btn btn-quiet" href="/#maker">جرّبوا أسماءكم على التعليقة</a></p>
  </div>
  <figure class="photo">{img("masaka-arous-4.webp", "مسكة عروس توليب مع تعليقة أكريليك بالأسماء")}</figure>
</div></section>

{section("قبل الحجز", promise_list(), cls="tint")}
<section class="section"><div class="container narrow">
  <h2>أسئلة عن مسكات العروس</h2>
  {faq_html(faqs)}
  {related("masakat")}
</div></section>"""
    sch = [bsch, faq_schema(faqs),
           product_schema("مسكة العروس", "مسكة عروس من الورد الصناعي عالي الجودة، 20 إلى 25 وردة: توليب، كريستال، كالا، جوري، بيوني، وألوان حسب الطلب.",
                          ["masaka-arous-crystal.webp", "masaka-arous-calla.webp", "masaka-arous-tulip.webp", "masaka-arous-1.webp"], P["masaka"], sku="masaka")]
    write(PAGES["masakat"]["path"], layout("masakat", PAGES["masakat"]["path"],
        f"مسكة عروس في الأردن بـ{P['masaka']} دينار: توليب، كريستال، كالا | هدايا سلمى",
        f"مسكات عروس توليب وكريستال وكالا وجوري وبيوني، ورد صناعي لا يذبل، {P['masaka']} دينار و{withdel('masaka')} مع التوصيل لكل محافظات الأردن. معاينة ودفع عند الاستلام.",
        body, sch, og_img="masaka-arous-crystal.webp"))

def build_style(s):
    trail = [(PAGES["masakat"]["nav"], PAGES["masakat"]["path"]), (s["nav"], s["path"])]
    head, bsch = page_intro(trail, s["h1"], s["lead"], "masaka")
    faqs = [(q, a or f"سعرها {P['masaka']} دينارًا، و{withdel('masaka')} دينارًا شاملة التوصيل إلى أي محافظة. والتعليقة بالأسماء +{P['taliqa']} دينار.")
            for q, a in s["faq"]] + [FAQ[7], FAQ[9], FAQ[6]]
    others = "".join(f'<a href="{o["path"]}">{E(o["nav"])}</a>' for o in STYLES if o is not s)
    paras = "".join(f"<p>{E(p)}</p>" for p in s["about"])
    body = head + f"""
<section class="section flush"><div class="container">{mosaic(s["photos"])}</div></section>
<section class="section"><div class="container narrow">
  <h2>عن مسكة ال{E(s['name'])}</h2>
  {paras}
  {promise_list()}
</div></section>
<section class="section"><div class="container narrow">
  <h2>أسئلة عن مسكة ال{E(s['name'])}</h2>
  {faq_html(faqs)}
  <nav class="related" aria-label="أنواع أخرى"><p>أنواع أخرى</p><div class="chips">{others}<a href="{PAGES['masakat']['path']}#peony">مسكة عروس بيوني</a></div></nav>
</div></section>"""
    sch = [bsch, faq_schema(faqs),
           product_schema(s["h1"], s["lead"], [p[0] for p in s["photos"]], P["masaka"], sku="masaka-" + s["key"])]
    write(s["path"], layout("style-" + s["key"], s["path"],
        f"{s['h1']} بـ{P['masaka']} دينار | هدايا سلمى، الأردن",
        f"{s['h1']}: {s['lead']} {P['masaka']} دينار و{withdel('masaka')} مع التوصيل لكل محافظات الأردن.",
        body, sch, og_img=s["photos"][0][0]))

# =====================================================================
# صواني الخطوبة
# =====================================================================
def build_sawani():
    head, bsch = page_intro([(PAGES["sawani"]["nav"], PAGES["sawani"]["path"])],
        "صينية خطوبة ودبل بالأسماء",
        "مرآة تحمل أسماءكم وتاريخ المناسبة، بظهر خشبي يحميها من الكسر، مع علبتين للخواتم بحروفكم الأولى، ولؤلؤ ودانتيل.",
        "saniya", extra=f'<p><a class="text-link" href="/#maker">جرّبوا أسماءكم على الصينية {ARROW}</a></p>')
    faqs = [FAQ[3], FAQ[5], FAQ[6], FAQ[7], FAQ[9]]
    adds = f"""<table class="prices"><tbody>
      <tr><td>حروفكم الأولى على علب الدبل</td><td>مجانًا</td></tr>
      <tr><td>ستاند أسود</td><td>+{P['stand']} دينار</td></tr>
      <tr><td>قصاصات</td><td>+{P['qassasat']} دنانير</td></tr>
      <tr><td>فناجين بالأسماء</td><td>+{P['fanajin']} دنانير</td></tr>
      <tr><td>قصاصة التقويم أو رسالة العمر</td><td>+{P['taqweem']} دينار</td></tr>
    </tbody></table>"""
    body = head + f"""
<section class="section flush"><div class="container">{mosaic([
        ("saniyet-khotoba-1.webp", "صينية خطوبة مرآة بالأسماء مع علب الدبل ولؤلؤ", "مرآة بالأسماء مع علب الدبل"),
        ("saniyet-khotoba-2.webp", "صينية دبل بالحروف والتاريخ", "بالحروف والتاريخ"),
        ("saniyet-khotoba-3.webp", "صينية دبل مرآة مع ورد ولؤلؤ", "مع ورد ولؤلؤ")])}</div></section>
<section class="section"><div class="container split">
  <div><h2>ماذا تتضمن</h2>{includes(["مرآة بأسمائكم وتاريخ المناسبة", "ظهر خشبي يحمي المرآة من الكسر", "آية، أو عبارة بدلًا منها حسب رغبتكم", "علبتان للخواتم بحروفكم الأولى", "شريط من اللؤلؤ والدانتيل بين الخواتم"])}</div>
  <div><h2>إضافات</h2>{adds}</div>
</div></section>
<section class="section tint"><div class="container narrow">
  <h2>هل تريدون الصينية مع كتاب عقد القران؟</h2>
  <p>اطلبوها ضمن بكج: بكج البرواز بسعر {P['bakj_berwaz']} دينارًا، أو البكج الأساسي بسعر {P['bakj_asasi']} دينارًا مع كتاب التوقيع والبصمات ورسالة العمر.</p>
  <p><a class="btn btn-quiet" href="{PAGES['bakjat']['path']}">تصفّحوا البكجات</a></p>
</div></section>
<section class="section"><div class="container narrow">
  <h2>أسئلة عن صواني الخطوبة</h2>
  {faq_html(faqs)}
  {related("sawani")}
</div></section>"""
    sch = [bsch, faq_schema(faqs),
           product_schema("صينية الخطوبة والدبل", "صينية من المرآة بظهر خشبي، بأسماء العروسين والتاريخ مع علبتين للخواتم ولؤلؤ ودانتيل.",
                          ["saniyet-khotoba-1.webp", "saniyet-khotoba-2.webp", "saniyet-khotoba-3.webp"], P["saniya"], sku="saniya")]
    write(PAGES["sawani"]["path"], layout("sawani", PAGES["sawani"]["path"],
        f"صينية خطوبة ودبل مرآة بالأسماء بـ{P['saniya']} دينار | هدايا سلمى",
        f"صواني خطوبة ودبل من المرآة بظهر خشبي، بأسماء العروسين والتاريخ مع علب الخواتم. {P['saniya']} دينار و{withdel('saniya')} مع التوصيل لكل الأردن، معاينة ودفع عند الاستلام.",
        body, sch, og_img="saniyet-khotoba-1.webp"))

# =====================================================================
# البكجات
# =====================================================================
def build_bakjat():
    def pkg(name, k, desc, inc, tag=""):
        t = f' <span class="tag">{E(tag)}</span>' if tag else ""
        return f"""<article class="pkg">
  <h3>{E(name)}{t}</h3>
  <p class="p-price"><b>{P[k]} <small>دينار</small></b><span>{withdel(k)} شاملة التوصيل</span></p>
  <p>{E(desc)}</p>
  {includes(inc)}
</article>"""
    pkgs = (pkg("بكج البرواز", "bakj_berwaz", "لمن يفضّل برواز بصمات يُعلَّق في المنزل بدلًا من الكتاب.", ["صينية الدبل بأسمائكم", "علب الخواتم بأحرفكم", "برواز بصمات بالأسماء", "حبر البصمات"])
            + pkg("البكج الأساسي", "bakj_asasi", "الأكثر طلبًا لعقد القران، ويضم كل ما تحتاجونه.", ["صينية الدبل بأسمائكم", "علب الخواتم بأحرفكم", "كتاب عقد الزواج والتوقيع والبصمات", "حبر البصمات", "رسالة العمر", "شريط لؤلؤ بين الخواتم"], tag="الأكثر طلبًا")
            + pkg("البكج الشامل", "bakj_shamel", "البكج الأساسي كاملًا، مع الفناجين والقصاصات.", ["كل محتويات البكج الأساسي", "فناجين بالأسماء", "قصاصات"]))
    faqs = [FAQ[4], FAQ[5], FAQ[7], FAQ[8], FAQ[9]]
    head, bsch = page_intro([(PAGES["bakjat"]["nav"], PAGES["bakjat"]["path"])],
        "بكجات كتب الكتاب: محتوياتها وأسعارها",
        f"كل ما تحتاجونه لعقد القران في طلب واحد، بأسمائكم وتاريخ مناسبتكم، من {P['bakj_berwaz']} إلى {P['bakj_shamel']} دينارًا.")
    body = head + f"""
<section class="section flush"><div class="container">{mosaic([("bakj-katb-ktab-2.webp", "البكج الأساسي لكتب الكتاب: صينية دبل وكتاب توقيع وبصمات", "البكج الأساسي"), ("bakj-katb-ktab-1.webp", "كتاب عقد الزواج بالأسماء", "كتاب عقد الزواج"), ("bakj-berwaz-1.webp", "بكج البرواز مع صينية الدبل", "بكج البرواز")])}</div></section>
<section class="section"><div class="container">
  <h2>اختاروا البكج المناسب</h2>
  <div class="pkgs">{pkgs}</div>
  <p class="section-intro">وإن أردتم كتاب التوقيع والبصمات وحده، فسعره {P['kitab']} دنانير، و{withdel('kitab')} دينارًا شاملة التوصيل.</p>
</div></section>
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
    write(PAGES["bakjat"]["path"], layout("bakjat", PAGES["bakjat"]["path"],
        f"بكج كتب الكتاب من {P['bakj_berwaz']} دينار | هدايا سلمى",
        f"بكجات كتب كتاب بالأسماء: بكج البرواز {P['bakj_berwaz']}، الأساسي {P['bakj_asasi']}، الشامل {P['bakj_shamel']} دينار. صينية دبل وكتاب بصمات ورسالة العمر، توصيل لكل الأردن.",
        body, sch, og_img="bakj-katb-ktab-2.webp"))

# =====================================================================
# صندوق المهر
# =====================================================================
def build_mahr():
    head, bsch = page_intro([(PAGES["mahr"]["nav"], PAGES["mahr"]["path"])],
        "صندوق المهر: أجمل طريقة لتقديم المهر للعروس",
        "صندوق فاخر بكامل زينته لتقديم المهر للعروس، ويمكن إضافة الأسماء أو عبارة عليه.",
        "mahr", extra='<p class="tag">الكمية محدودة، تواصلوا معنا للتأكد من التوفر</p>')
    faqs = [("كم سعر صندوق المهر؟", f"سعره {P['mahr']} دينارًا، و{withdel('mahr')} دينارًا شاملة التوصيل إلى جميع محافظات الأردن. الكمية محدودة، لذا تواصلوا معنا للتأكد من التوفر."),
            FAQ[6], FAQ[8], FAQ[9]]
    body = head + f"""
<section class="section flush"><div class="container">{mosaic([("sandouq-mahr-1.webp", "صندوق مهر خشبي فاخر لتقديم المهر للعروس", "صندوق المهر")])}</div></section>
{section("قبل الحجز", promise_list(), cls="tint")}
<section class="section"><div class="container narrow">
  <h2>أسئلة عن صندوق المهر</h2>
  {faq_html(faqs)}
  {related("mahr")}
</div></section>"""
    sch = [bsch, faq_schema(faqs),
           product_schema("صندوق المهر", "صندوق فاخر لتقديم المهر للعروس، شامل كامل الزينة والإكسسوارات.", ["sandouq-mahr-1.webp"], P["mahr"],
                          avail="https://schema.org/LimitedAvailability", sku="mahr")]
    write(PAGES["mahr"]["path"], layout("mahr", PAGES["mahr"]["path"],
        f"صندوق المهر بسعر {P['mahr']} دينار | هدايا سلمى",
        f"صندوق مهر فاخر لتقديم المهر للعروس مع كامل الزينة، {P['mahr']} دينار و{withdel('mahr')} مع التوصيل لكل محافظات الأردن. حسب التوفر.",
        body, sch, og_img="sandouq-mahr-1.webp"))

# =====================================================================
# التخرج
# =====================================================================
def build_grad():
    head, bsch = page_intro([(PAGES["grad"]["nav"], PAGES["grad"]["path"])],
        "هدايا تخرج بالاسم: صينية التخرج",
        "صينية باسم الخريج أو الخريجة والتخصص، مع ورد وزينة.", "takharroj")
    faqs = [FAQ[12], FAQ[6], FAQ[7], FAQ[8], FAQ[9]]
    body = head + f"""
<section class="section flush"><div class="container">{mosaic([("hadiyet-takharroj-1.webp", "صينية تخرج باسم الخريجة والتخصص", "صينية التخرج")])}</div></section>
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
    write(PAGES["grad"]["path"], layout("grad", PAGES["grad"]["path"],
        f"هدية تخرج بالاسم: صينية تخرج بسعر {P['takharroj']} دينار | هدايا سلمى",
        f"صينية تخرج باسم الخريج أو الخريجة والتخصص، {P['takharroj']} دينار و{withdel('takharroj')} مع التوصيل لكل محافظات الأردن. معاينة ودفع عند الاستلام.",
        body, sch, og_img="hadiyet-takharroj-1.webp"))

# =====================================================================
# الأسعار والتوصيل
# =====================================================================
def build_tawseel():
    bc, bsch = bc_page("tawseel")
    rows = [("مسكة العروس (كل الأنواع)", "masaka", PAGES["masakat"]["path"]), ("صينية الخطوبة / الدبل", "saniya", PAGES["sawani"]["path"]),
            ("بكج البرواز", "bakj_berwaz", PAGES["bakjat"]["path"]), ("البكج الأساسي", "bakj_asasi", PAGES["bakjat"]["path"]),
            ("البكج الشامل", "bakj_shamel", PAGES["bakjat"]["path"]), ("كتاب أو دفتر توقيع منفرد", "kitab", PAGES["bakjat"]["path"]),
            ("صندوق المهر (حسب التوفر)", "mahr", PAGES["mahr"]["path"]), ("صينية التخرج", "takharroj", PAGES["grad"]["path"])]
    tr = "".join(f'<tr><td><a href="{u}">{E(n)}</a></td><td>{P[k]} دينار</td><td>{withdel(k)} دينار</td></tr>' for n, k, u in rows)
    adds = [("تعليقة للمسكة", "taliqa"), ("ستاند أسود", "stand"), ("قصاصات", "qassasat"), ("فناجين", "fanajin"), ("قصاصة التقويم أو رسالة العمر", "taqweem")]
    ta = "".join(f"<tr><td>{E(n)}</td><td>+{P[k]} دينار</td></tr>" for n, k in adds)
    govs = "عمّان، الزرقاء، إربد، السلط، مأدبا، جرش، عجلون، المفرق، الكرك، الطفيلة، معان، العقبة"
    body = bc + f"""
<section class="p-head container">
  <h1>أسعار مسكات العروس وصواني الخطوبة، والتوصيل</h1>
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
    write(PAGES["tawseel"]["path"], layout("tawseel", PAGES["tawseel"]["path"],
        "أسعار مسكة العروس وصينية الخطوبة والتوصيل 2026 | هدايا سلمى",
        f"أسعار مسكات العروس ({P['masaka']} دينار) وصواني الخطوبة ({P['saniya']}) والبكجات، والتوصيل لكل محافظات الأردن بسعر {DELIVERY} دينار خلال يومين. دفع ومعاينة عند الاستلام.",
        body, [bsch]))

# =====================================================================
# الأسئلة الشائعة
# =====================================================================
def build_faq():
    bc, bsch = bc_page("faq")
    body = bc + f"""
<section class="p-head container">
  <h1>أسئلة شائعة عن هدايا سلمى</h1>
  <p class="lead">أكثر الأسئلة التي تصلنا عن المسكات والصواني والبكجات والأسعار والتوصيل. إن لم تجدوا سؤالكم هنا، تواصلوا معنا على إنستغرام.</p>
</section>
<section class="section"><div class="container narrow">
  {faq_html(FAQ)}
  {related("faq")}
</div></section>"""
    write(PAGES["faq"]["path"], layout("faq", PAGES["faq"]["path"],
        "أسئلة شائعة: أسعار المسكات والصواني والتوصيل | هدايا سلمى",
        "من أين أشتري مسكة عروس في الأردن؟ كم سعر صينية الخطوبة؟ هل يصل التوصيل إلى جميع المحافظات؟ جميع الإجابات عن هدايا سلمى في مكان واحد.",
        body, [bsch, faq_schema(FAQ)]))

# =====================================================================
# 404
# =====================================================================
def build_404():
    body = f"""<section class="p-head container">
  <h1>الصفحة غير موجودة</h1>
  <p class="lead">ربما تغيّر الرابط. عودوا إلى الصفحة الرئيسية أو اختاروا إحدى الصفحات أدناه.</p>
  <p><a class="btn btn-quiet" href="/">الرئيسية</a></p>
  {related(None)}
</section>"""
    out = layout("404", "/404.html", "الصفحة غير موجودة | هدايا سلمى", "الصفحة المطلوبة غير موجودة.", body, [])
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(out)

# =====================================================================
# sitemap + llms.txt
# =====================================================================
def all_paths():
    return [PAGES[k]["path"] for k in ["home"] + NAV_ORDER] + [s["path"] for s in STYLES]

def build_sitemap():
    urls = "".join(f"  <url><loc>{SITE}{p}</loc><lastmod>{TODAY}</lastmod></url>\n" for p in all_paths())
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')

def build_llms():
    lines = [
        "# Salma Gifts - هدايا سلمى",
        "",
        f"> متجر أردني أونلاين لهدايا المناسبات حسب الطلب: مسكات العروس (توليب، كريستال، كالا، جوري، بيوني — ورد صناعي لا يذبل)، صواني الخطوبة والدبل من المرآة بالأسماء، بكجات كتب الكتاب، صندوق المهر وهدايا التخرج. توصيل لكل محافظات الأردن، ومعاينة ودفع عند الاستلام. الطلب عبر رسائل إنستغرام @salma.gifts1. شعارنا: {SLOGAN}",
        "",
        "Salma Gifts is an online gift shop in Jordan making personalized engagement and wedding items: artificial-flower bridal bouquets (tulip, crystal, calla, rose/jouri, peony; any color to match the dress), mirror engagement ring trays with the couple's names (wooden back against breaking), marriage-contract (katb el-kitab) signature book packages, dowry (mahr) boxes and graduation gifts. 1500+ orders completed, 120+ orders a week. Delivery to all governorates of Jordan for 2 JOD within two days. Cash on delivery with inspection before paying. Orders via Instagram DM @salma.gifts1.",
        "",
        "## الأسعار (دينار أردني، بدون التوصيل)",
        f"- مسكة العروس، كل الأنواع: {P['masaka']} (ورد صناعي عالي الجودة، 20–25 وردة). تعليقة بالأسماء والتاريخ: +{P['taliqa']}",
        f"- صينية الخطوبة / الدبل (مرآة بظهر خشبي، بالأسماء والتاريخ، مع علب الخواتم): {P['saniya']}",
        f"- بكج البرواز (صينية + برواز بصمات): {P['bakj_berwaz']}",
        f"- البكج الأساسي (صينية + كتاب توقيع وبصمات + رسالة العمر + حبر): {P['bakj_asasi']}",
        f"- البكج الشامل (الأساسي + فناجين + قصاصات): {P['bakj_shamel']}",
        f"- كتاب / دفتر توقيع منفرد: {P['kitab']}",
        f"- صندوق المهر (حسب التوفر): {P['mahr']}",
        f"- صينية التخرج بالاسم والتخصص: {P['takharroj']}",
        f"- التوصيل لأي محافظة: {DELIVERY}",
        "",
        "## أنواع مسكات العروس",
    ] + [f"- [{s['nav']}]({SITE}{s['path']}): {s['lead']}" for s in STYLES] + [
        f"- مسكة عروس بيوني: بيوني أبيض مع جبسوفيل، أو بالوردي حسب الطلب ({SITE}{PAGES['masakat']['path']}#peony)",
        "",
        "## السياسات",
        "- الطلب يجهز ويوصل خلال يومين كحد أقصى، والحجز قبل المناسبة بثلاثة أيام على الأقل.",
        "- الدفع عند الاستلام (كاش أو كليك)، مع معاينة قبل الدفع؛ إذا لم يعجب الطلب يُرجع ويُدفع التوصيل فقط.",
        "- أونلاين فقط، لا يوجد محل. التواصل عبر إنستغرام أو ماسنجر.",
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
    build_home(); build_masakat()
    for s in STYLES:
        build_style(s)
    build_sawani(); build_bakjat(); build_mahr(); build_grad()
    build_tawseel(); build_faq(); build_404(); build_sitemap(); build_llms()
    print("تم بناء الموقع.")
