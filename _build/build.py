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
VERSION = "23"  # غيّره لما تعدّل style.css أو main.js عشان المتصفحات تجيب النسخة الجديدة
SLOGAN = "لتبقى ذكرياتكم الجميلة، خالدة."
GA_ID = ""  # Google Analytics 4 (G-XXXX). فاضي = بدون تتبّع
CLARITY_ID = "z16hn3m2mn"  # Microsoft Clarity: الزوار، الكبسات، تسجيلات الجلسات

# =====================================================================
# الأسعار — المصدر الوحيد. غيّر الرقم هون بس.
# =====================================================================
PRICES = {
    "masaka": 18,        # مسكة العروس (عرض خاص)
    "masaka_old": 25,    # سعرها قبل العرض الدائم (قرار سامي 31/10)
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
SALE_PCT = round((P["masaka_old"] - P["masaka"]) * 100 / P["masaka_old"])

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
               "الورد صناعي عالي الجودة فلا يذبل، وتبقى المسكة ذكرى في بيتكم بعد المناسبة."],
     "photos": [("sowar/maska-03.webp", "مسكة عروس توليب أبيض بالكريستال ومقبض ستراس", "توليب بالكريستال"), ("masaka-arous-tulip.webp", "مسكة عروس توليب أبيض بقاعدة ستراس ولولو", "توليب بقاعدة ستراس"),
                ("masaka-arous-trend.webp", "مسكة عروس توليب مع لولو", "توليب مع لولو"),
                ("masaka-arous-4.webp", "مسكة عروس توليب أبيض", "توليب أبيض")],
     "faq": [("كم سعر مسكة العروس التوليب؟", None), ("هل التوليب طبيعي؟", "لا، توليب صناعي عالي الجودة يشبه الطبيعي ولا يذبل، فيبقى بحالته بعد المناسبة.")]},
    {"key": "crystal", "path": "/masakat-arayes/crystal/", "name": "كريستال", "nav": "مسكة عروس كريستال",
     "h1": "مسكة عروس كريستال",
     "lead": "توليب أبيض تحيطه حبّات كريستال ولولو، تلمع مع كل حركة. لمن تريد مسكة فخمة دون مبالغة.",
     "about": ["تُلفّ المسكة بتل شفاف ناعم، وتتوزّع حبّات الكريستال واللولو بين الورد بتنسيق متناسق. ويمكن اختيار كمية الكريستال وتوزيعه حسب رغبتكم.",
               "مثل باقي مسكاتنا، تُجهَّز كل واحدة على حدة وتصلكم خلال يومين، وتعاينونها قبل الدفع."],
     "photos": [("sowar/maska-02.webp", "مسكة عروس توليب أبيض بإطار كريستال", "توليب بإطار كريستال"), ("masaka-arous-crystal.webp", "مسكة عروس توليب بالكريستال", "توليب بالكريستال"),
                ("masaka-arous-crystal-2.webp", "مسكة عروس توليب بحبات الكريستال على السيقان", "حبّات الكريستال على السيقان"),
                ("masaka-arous-crystal-detail.webp", "تفاصيل مسكة عروس بالكريستال واللولو والتل", "كريستال ولولو وتل")],
     "faq": [("كم سعر مسكة العروس الكريستال؟", None), ("هل يمكن زيادة الكريستال؟", "نعم، أخبرونا عند الطلب بالكمية والتوزيع الذي تفضّلونه، ونجهّزها على هذا الأساس.")]},
    {"key": "calla", "path": "/masakat-arayes/calla/", "name": "كالا", "nav": "مسكة عروس كالا",
     "h1": "مسكة عروس كالا",
     "lead": "زهر الكالا الأبيض بخطوطه الطويلة يعطي المسكة أناقة ملكية، وحده أو مع الجوري الملوّن.",
     "about": ["نجهّز الكالا بقاعدة من اللولو أو الستراس، أو نمزجه مع الجوري الأزرق أو بلون يناسب فستانكم.",
               "والكالا صناعي عالي الجودة لا يذبل، فيمكن الاحتفاظ بالمسكة بعد المناسبة."],
     "photos": [("sowar/maska-05.webp", "مسكة عروس كالا أبيض", "كالا أبيض"), ("masaka-arous-calla.webp", "مسكة عروس كالا بيضاء مع لولو", "كالا أبيض مع لولو"),
                ("masaka-arous-calla-blue.webp", "مسكة عروس كالا مع جوري أزرق وجبسوفيل", "كالا مع جوري أزرق"),
                ("masaka-arous-3.webp", "مسكة عروس كالا طويلة بقاعدة ستراس", "كالا طويلة"),
                ("masaka-arous-2.webp", "مسكات عروس كالا بقاعدة لولو", "كالا بقاعدة لولو")],
     "faq": [("كم سعر مسكة العروس الكالا؟", None), ("هل يمكن مزج الكالا مع ورد ملوّن؟", "نعم، مثل الكالا مع الجوري الأزرق، أو بأي لون يناسب فستانكم.")]},
    {"key": "jouri", "path": "/masakat-arayes/jouri/", "name": "جوري", "nav": "مسكة عروس جوري",
     "h1": "مسكة عروس جوري",
     "lead": "الجوري مع الجبسوفيل: رقّة وأنوثة، بالأبيض أو بلون تختارونه.",
     "about": ["نجهّز مسكة الجوري بالأبيض الكلاسيكي مع الجبسوفيل، أو بالأزرق مع الكالا، أو بلون يناسب فستانكم.",
               "تُلفّ القاعدة بالستراس أو التل أو اللولو حسب رغبتكم، وتُجهَّز كل مسكة على حدة."],
     "photos": [("sowar/maska-01.webp", "مسكة عروس جوري أبيض مع جبسوفيل وفيونكة دانتيل", "جوري مع جبسوفيل"), ("masaka-arous-jouri.webp", "مسكات عروس جوري أبيض مع جبسوفيل", "جوري مع جبسوفيل"),
                ("masaka-arous-calla-blue.webp", "مسكة عروس جوري أزرق مع كالا", "جوري أزرق مع كالا")],
     "faq": [("كم سعر مسكة العروس الجوري؟", None), ("هل يتوفر الجوري بألوان؟", "نعم، الأبيض هو الأكثر طلبًا، ونجهّز الأزرق والوردي وأي لون يناسب فستانكم.")]},
    {"key": "khotoba", "path": "/masakat-arayes/khotoba/", "name": "خطوبة", "nav": "مسكة خطوبة",
     "h1": "مسكة خطوبة",
     "lead": "مسكات خطوبة بالأبيض أو بألوان ناعمة تناسب فستان الخطوبة: زهري، أزرق، وألوان هادئة، مع لولو أو دانتيل.",
     "about": ["نجهّز مسكة الخطوبة من نفس ورد مسكات العروس: توليب وكالا وجوري وبيوني، ونختار معكم الألوان لتتناسق مع فستان الخطوبة.",
               "الورد صناعي عالي الجودة لا يذبل، فتبقى المسكة ذكرى من يوم الخطوبة."],
     "photos": [("sowar/maska-24.webp", "مسكة خطوبة بألوان ناعمة باللولو", "ألوان ناعمة باللولو"), ("sowar/maska-20.webp", "مسكة خطوبة جربيرا وجوري بألوان ناعمة", "جربيرا وجوري"),
                ("sowar/maska-18.webp", "مسكة خطوبة كالا وجوري زهري", "كالا وجوري زهري"),
                ("sowar/maska-04.webp", "مسكة خطوبة كالا وجوري أزرق", "كالا وجوري أزرق")],
     "faq": [("كم سعر مسكة الخطوبة؟", None), ("هل يمكن اختيار لون مسكة الخطوبة؟", "نعم، نجهّزها بالأبيض أو بأي لون يناسب فستان الخطوبة، بالسعر نفسه.")]},
]
# =====================================================================
# موديلات المسكات — كل موديل صفحة (الأسماء والصور من ملف سامي 23/10، 18 موديل)
# =====================================================================
MODELS_PATH = "/masakat-arayes/mawdeelat/"
MODELS = [
    {"slug": 'toulib-lulu', "name": 'توليب اللولو', "h1": 'مسكة عروس توليب باللولو', "style": 'tulip', "w": 900, "h": 1141,
     "lead": 'توليب أبيض تحيط به حبّات اللولو والكريستال، مع كشكش من التل الناعم، ومسكة مغطاة باللولو بالكامل. فخامة هادئة.',
     "inc": ['توليب أبيض صناعي عالي الجودة', 'إطار من حبّات اللولو والكريستال حول الورد', 'كشكش من التل الناعم', 'مسكة مغطاة باللولو بالكامل']},
    {"slug": 'kala-toulib-crystal', "name": 'كالا وتوليب بالكريستال', "h1": 'مسكة عروس كالا وتوليب بالكريستال', "style": 'calla', "w": 900, "h": 1141,
     "lead": 'كالا أبيض حول قلب من التوليب، وبين الورد حبّات لولو وكريستال، ومسكة من الستراس الفضي تلمع في كل صورة.',
     "inc": ['قلب من التوليب الأبيض', 'كالا أبيض حول التوليب', 'حبّات لولو وكريستال بين الورد', 'مسكة من الستراس الفضي']},
    {"slug": 'kala-zahr-wardi', "name": 'كالا والزهر الوردي', "h1": 'مسكة عروس كالا مع زهر وردي', "style": 'calla', "w": 900, "h": 1141,
     "lead": 'كالا أبيض مع زهور وردية فاتحة في الوسط، ومسكة ملفوفة بالأبيض. لمسة لون ناعمة على المسكة البيضاء.',
     "inc": ['كالا أبيض صناعي عالي الجودة', 'زهور وردية فاتحة بين الكالا', 'مسكة ملفوفة بالأبيض']},
    {"slug": 'jouri-zahri-toulib', "name": 'جوري زهري وتوليب', "h1": 'مسكة عروس جوري زهري وتوليب', "style": 'jouri', "w": 900, "h": 1141,
     "lead": 'جوري زهري في الوسط، يحيط به توليب وكالا أبيض، مع دانتيل على المسكة. لعروس تحب اللون الهادئ.',
     "inc": ['جوري زهري في الوسط', 'توليب وكالا أبيض حوله', 'مسكة ملفوفة بالدانتيل']},
    {"slug": 'toulib-classic', "name": 'توليب كلاسيك', "h1": 'مسكة عروس توليب كلاسيك', "style": 'tulip', "w": 900, "h": 1141,
     "lead": 'توليب أبيض بسيقان خضراء طويلة ظاهرة، مربوط بشريطة بيضاء. بسيطة وأنيقة.',
     "inc": ['توليب أبيض صناعي عالي الجودة', 'سيقان خضراء طويلة ظاهرة', 'ربطة بيضاء على المسكة']},
    {"slug": 'toulib-gypsophila', "name": 'توليب والجبسوفيل', "h1": 'مسكة عروس توليب وجبسوفيل', "style": 'tulip', "w": 900, "h": 1003,
     "lead": 'توليب أبيض يحتضنه ورد الجبسوفيل (بيبي بريث) الناعم، ومسكة من الدانتيل. رقيقة وطبيعية.',
     "inc": ['توليب أبيض صناعي عالي الجودة', 'ورد الجبسوفيل حول التوليب', 'مسكة ملفوفة بالدانتيل']},
    {"slug": 'toulib-crystal', "name": 'توليب الكريستال', "h1": 'مسكة عروس توليب بالكريستال', "style": 'crystal', "w": 900, "h": 1141,
     "lead": 'توليب أبيض فوق إكليل من الكريستال واللولو، مع أسلاك فضية ومسكة من الستراس. لمن تريد اللمعة.',
     "inc": ['توليب أبيض صناعي عالي الجودة', 'إكليل من الكريستال واللولو تحت الورد', 'أسلاك فضية', 'مسكة من الستراس']},
    {"slug": 'kala-gypsophila', "name": 'كالا والجبسوفيل', "h1": 'مسكة عروس كالا وجبسوفيل', "style": 'calla', "w": 900, "h": 688,
     "lead": 'كالا أبيض كثيف يحيط به الجبسوفيل الأبيض، بسيقان خضراء. ناعمة وممتلئة.',
     "inc": ['كالا أبيض صناعي عالي الجودة', 'جبسوفيل حول الكالا', 'سيقان خضراء']},
    {"slug": 'jouri-abyad', "name": 'جوري أبيض كلاسيك', "h1": 'مسكة عروس جوري أبيض كلاسيك', "style": 'jouri', "w": 900, "h": 688,
     "lead": 'جوري أبيض كثيف بشكل دائري يتخلّله الجبسوفيل. مسكة كلاسيكية ناعمة تليق بكل فستان أبيض.',
     "inc": ['جوري أبيض صناعي عالي الجودة', 'تنسيق دائري كثيف', 'جبسوفيل بين الورد']},
    {"slug": 'peony-boho', "name": 'بيوني بوهو', "h1": 'مسكة عروس بيوني بوهو', "style": 'peony', "w": 900, "h": 688,
     "lead": 'بيوني وردي فاتح في الوسط مع زهور بيضاء وجبسوفيل، وخيوط لولو متدلية ومسكة بشريطة. ستايل بوهو ناعم.',
     "inc": ['بيوني وردي فاتح في الوسط', 'زهور بيضاء وجبسوفيل', 'خيوط لولو متدلية', 'مسكة ملفوفة بشريطة']},
    {"slug": 'turkish-qaws', "name": 'المسكة التركية (القوس)', "h1": 'مسكة عروس تركية على شكل قوس', "style": 'calla', "w": 900, "h": 825,
     "lead": 'كالا أبيض ينسدل على شكل قوس، بمسكة من اللولو وفيونكة من التل وخيوط لولو. ستايل مختلف ولافت.',
     "inc": ['كالا أبيض منسدل على شكل قوس', 'مسكة من اللولو', 'فيونكة من التل', 'خيوط لولو متدلية']},
    {"slug": 'toulib-organza', "name": 'توليب الأورجانزا', "h1": 'مسكة عروس توليب بالأورجانزا', "style": 'tulip', "w": 900, "h": 1109,
     "lead": 'توليب أبيض ملفوف بقماش الأورجانزا المكشكش ومربوط بشريطة. شكل فخم مثل فستان العروس.',
     "inc": ['توليب أبيض صناعي عالي الجودة', 'لفّة من الأورجانزا المكشكشة', 'ربطة بشريطة']},
    {"slug": 'peony-abyad-gypsophila', "name": 'بيوني أبيض والجبسوفيل', "h1": 'مسكة عروس بيوني أبيض وجبسوفيل', "style": 'peony', "w": 900, "h": 1141,
     "lead": 'بيوني أبيض ممتلئ مع الجبسوفيل، ومسكة ملفوفة بالأبيض. ناعمة وكلاسيكية.',
     "inc": ['بيوني أبيض صناعي عالي الجودة', 'جبسوفيل بين الورد', 'مسكة ملفوفة بالأبيض']},
    {"slug": 'kala-classic-strass', "name": 'كالا كلاسيك بالستراس', "h1": 'مسكة عروس كالا كلاسيك بالستراس', "style": 'calla', "w": 900, "h": 1141,
     "lead": 'كالا أبيض بسيقان طويلة، ومسكة ملفوفة بالستراس اللامع. أناقة بسيطة بلمعة.',
     "inc": ['كالا أبيض صناعي عالي الجودة', 'سيقان طويلة', 'مسكة ملفوفة بالستراس']},
    {"slug": 'toulib-tul', "name": 'توليب ملفوف بالتول', "h1": 'مسكة عروس توليب ملفوف بالتول', "style": 'tulip', "w": 900, "h": 1141,
     "lead": 'توليب أبيض ملفوف بطبقات من التول الأبيض ومربوط بالدانتيل. خفيفة ورقيقة.',
     "inc": ['توليب أبيض صناعي عالي الجودة', 'لفّة من التول الأبيض', 'ربطة دانتيل']},
    {"slug": 'zahri-naem', "name": 'الزهري الناعم', "h1": 'مسكة عروس زهري ناعم', "style": 'other', "w": 900, "h": 1141,
     "lead": 'زهور زهرية ناعمة بقلوب داكنة، بمسكة من اللولو. لعروس تحب اللون.',
     "inc": ['زهور زهرية ناعمة بقلوب داكنة', 'مسكة من اللولو']},
    {"slug": 'kala-jouri-azraq', "name": 'كالا والجوري الأزرق', "h1": 'مسكة عروس كالا وجوري أزرق', "style": 'calla', "w": 900, "h": 1141,
     "lead": 'كالا أبيض مع ورد أزرق وجبسوفيل. مسكة ملوّنة لافتة للحنّة أو للعروس التي تحب الأزرق.',
     "inc": ['كالا أبيض صناعي عالي الجودة', 'ورد أزرق بين الكالا', 'جبسوفيل']},
    {"slug": 'qaws-toulib', "name": 'قوس التوليب', "h1": 'مسكة عروس قوس التوليب', "style": 'tulip', "w": 900, "h": 1141,
     "lead": 'توليب أبيض صغير ينسدل على شكل قوس، مع خيوط لولو وفيونكة من التل الأبيض.',
     "inc": ['توليب أبيض صغير منسدل على شكل قوس', 'خيوط لولو', 'فيونكة من التل الأبيض']},
]
# =====================================================================
# كتالوج المسكات — صور الستوديو الـ25 (ملف سامي 11/11). كل مسكة إلها صفحة.
# بدون أرقام موديلات: صورة كبيرة، اسم، سطرين وصف، سعر. (طلب سامي 14/11)
# =====================================================================
CATALOG = [
 {"n": "01", "slug": "jouri-abyad", "style": "jouri", "name": "جوري أبيض مع جبسوفيل",
  "lead": "جوري أبيض كثيف بتنسيق دائري، يتخلّله الجبسوفيل الناعم، ومسكة ملفوفة بفيونكة دانتيل. كلاسيكية تليق بكل فستان أبيض.",
  "inc": ["جوري أبيض صناعي عالي الجودة", "جبسوفيل بين الورد", "فيونكة دانتيل على المسكة"]},
 {"n": "02", "slug": "toulib-crystal", "style": "crystal", "name": "توليب أبيض بإطار كريستال",
  "lead": "توليب أبيض يحيط به إطار من حبّات الكريستال واللولو، ومسكة ستراس فضية تلمع مع كل حركة. من أكثر المسكات طلبًا.",
  "inc": ["توليب أبيض صناعي عالي الجودة", "إطار كريستال ولولو حول الورد", "مسكة ستراس فضية"]},
 {"n": "03", "slug": "toulib-crystal-strass", "style": "crystal", "name": "توليب بالكريستال ومقبض ستراس",
  "lead": "رأس كثيف من التوليب الأبيض بحافة كريستال، وسيقان خضراء طويلة يلفّها حزام ستراس. فخمة وأنيقة.",
  "inc": ["توليب أبيض كثيف", "حافة من حبّات الكريستال", "سيقان خضراء مع حزام ستراس"]},
 {"n": "04", "slug": "kala-jouri-azraq", "style": "calla", "name": "كالا وجوري أزرق",
  "lead": "جوري أزرق فاتح بجانب كالا أبيض وجبسوفيل، ومسكة ملفوفة بالساتان الأبيض. لمسة لون هادئة تناسب الخطوبة والحنّة.",
  "inc": ["جوري أزرق فاتح", "كالا أبيض وجبسوفيل", "مسكة ملفوفة بالساتان"]},
 {"n": "05", "slug": "kala-abyad", "style": "calla", "name": "كالا أبيض",
  "lead": "كالا أبيض بخطوطه الطويلة المتموّجة، وسيقان خضراء ظاهرة مربوطة بشريطة ساتان. بسيطة وراقية.",
  "inc": ["كالا أبيض صناعي عالي الجودة", "سيقان خضراء ظاهرة", "ربطة ساتان بيضاء"]},
 {"n": "06", "slug": "toulib-halaqa-lulu", "style": "tulip", "name": "توليب بمقبض حلقة لولو",
  "lead": "توليب أبيض ممتلئ مع لمسات كريستال، ومقبض على شكل حلقة من اللولو يسهل حمله. تصميم مختلف وعصري.",
  "inc": ["توليب أبيض صناعي", "لمسات كريستال بين الورد", "مقبض حلقة من اللولو"]},
 {"n": "07", "slug": "peony-lulu", "style": "peony", "name": "بيوني أبيض باللولو",
  "lead": "زهور بيوني بيضاء كبيرة ومفتوحة، ومسكة ملفوفة بالأبيض تتدلّى منها حبّات اللولو. ناعمة وممتلئة.",
  "inc": ["بيوني أبيض صناعي عالي الجودة", "مسكة ملفوفة بالأبيض", "خيوط لولو متدلية"]},
 {"n": "08", "slug": "toulib-lulu", "style": "tulip", "name": "توليب باللولو والجبسوفيل",
  "lead": "توليب أبيض يحيط به إطار من اللولو والجبسوفيل، مع كشكش من التل الناعم ومسكة ملفوفة بالتل. فخامة هادئة.",
  "inc": ["توليب أبيض صناعي", "إطار لولو وجبسوفيل", "كشكش ومسكة من التل"]},
 {"n": "09", "slug": "toulib-boutonniere", "style": "tulip", "name": "توليب مع بوتونيير للعريس",
  "lead": "مسكة توليب أبيض ملفوفة بالتل وفيونكة دانتيل، ومعها بوتونيير صغير مطابق لبدلة العريس.",
  "inc": ["مسكة توليب أبيض", "تل وفيونكة دانتيل", "بوتونيير مطابق للعريس"]},
 {"n": "10", "slug": "kala-lulu-crystal", "style": "calla", "name": "كالا باللولو ومقبض كريستال",
  "lead": "رأس دائري من الكالا الأبيض تتخلّله حبّات اللولو، ومقبض شفاف من الكريستال. تصميم ملكي لافت.",
  "inc": ["كالا أبيض بتنسيق دائري", "حبّات لولو بين الورد", "مقبض كريستال شفاف"]},
 {"n": "11", "slug": "kala-classic-strass", "style": "calla", "name": "كالا أبيض بمقبض ستراس",
  "lead": "كالا أبيض منسدل مع لمسات كريستال، ومسكة طويلة مغطاة بالستراس الفضي. أناقة كلاسيكية.",
  "inc": ["كالا أبيض صناعي", "لمسات كريستال", "مسكة ستراس فضية"]},
 {"n": "12", "slug": "kala-toulib-crystal", "style": "calla", "name": "كالا وتوليب بالكريستال",
  "lead": "كالا أبيض حول قلب من التوليب، وبين الورد حبّات كريستال، ومسكة من الستراس الفضي تلمع في كل صورة.",
  "inc": ["قلب من التوليب الأبيض", "كالا أبيض حوله", "مسكة ستراس فضية"]},
 {"n": "13", "slug": "kala-dantel", "style": "calla", "name": "كالا أبيض بمقبض دانتيل",
  "lead": "كالا أبيض كثيف بخطوط ناعمة، ومسكة ملفوفة بالدانتيل الأبيض وسيقان خضراء. رقيقة وأنثوية.",
  "inc": ["كالا أبيض صناعي", "مسكة دانتيل بيضاء", "سيقان خضراء ظاهرة"]},
 {"n": "14", "slug": "kala-aghsan", "style": "calla", "name": "كالا أبيض مع أغصان ناعمة",
  "lead": "كالا أبيض تحيط به أغصان بيضاء ناعمة متطايرة، ومسكة ملفوفة بالأبيض. ستايل بوهو هادئ.",
  "inc": ["كالا أبيض صناعي", "أغصان ناعمة حول الورد", "مسكة ملفوفة بالأبيض"]},
 {"n": "15", "slug": "kala-jouri-abyad", "style": "calla", "name": "كالا وجوري أبيض",
  "lead": "جوري أبيض بين الكالا، مع لمسات من الأعشاب الناعمة ومسكة ساتان بيضاء. متوازنة وأنيقة.",
  "inc": ["كالا وجوري أبيض", "لمسات أعشاب ناعمة", "مسكة ساتان بيضاء"]},
 {"n": "16", "slug": "jouri-fyonka", "style": "jouri", "name": "جوري أبيض بفيونكة دانتيل",
  "lead": "جوري أبيض كثيف مع الجبسوفيل، ومسكة يلفّها شريط دانتيل طويل بفيونكة. ناعمة وكلاسيكية.",
  "inc": ["جوري أبيض صناعي", "جبسوفيل", "فيونكة دانتيل طويلة"]},
 {"n": "17", "slug": "toulib-lulu-crystal", "style": "tulip", "name": "توليب باللولو والكريستال",
  "lead": "توليب أبيض بإطار من حبّات اللولو والكريستال المتدلية، ومسكة ستراس على سيقان خضراء. فخمة ومميزة.",
  "inc": ["توليب أبيض صناعي", "حبّات لولو وكريستال متدلية", "مسكة ستراس"]},
 {"n": "18", "slug": "kala-zahr-wardi", "style": "calla", "name": "كالا وجوري زهري",
  "lead": "جوري زهري فاتح في الوسط، يحيط به كالا وتوليب أبيض، ومسكة ملفوفة بالدانتيل. لعروس تحب اللون الهادئ.",
  "inc": ["جوري زهري فاتح", "كالا وتوليب أبيض", "مسكة دانتيل"]},
 {"n": "19", "slug": "toulib-tul", "style": "tulip", "name": "توليب ناعم ملفوف بالتل",
  "lead": "توليب أبيض مع حبّات لولو صغيرة، ملفوف بطبقات من التل الناعم حتى المسكة. خفيفة وحالمة.",
  "inc": ["توليب أبيض صناعي", "حبّات لولو صغيرة", "لفّة تل ناعمة"]},
 {"n": "20", "slug": "zahri-naem", "style": "khotoba", "name": "جربيرا وجوري بألوان ناعمة",
  "lead": "جربيرا وجوري بدرجات الخوخي والزهري الفاتح، مع الجبسوفيل وخيوط لولو. مبهجة وتناسب الخطوبة.",
  "inc": ["جربيرا وجوري بألوان ناعمة", "جبسوفيل", "خيوط لولو"]},
 {"n": "21", "slug": "qaws-toulib", "style": "tulip", "name": "قوس التوليب باللولو",
  "lead": "توليب أبيض منسدل على شكل قوس، تتدلّى بينه خيوط اللولو، ومقبض حلقة لولو مع فيونكة تل.",
  "inc": ["توليب أبيض منسدل", "خيوط لولو", "مقبض حلقة لولو وفيونكة"]},
 {"n": "22", "slug": "toulib-maqbad-lulu", "style": "tulip", "name": "توليب أبيض بمقبض لولو",
  "lead": "توليب أبيض بحافة دانتيل ولولو، ومسكة مغطاة بصفوف من اللولو. ناعمة ومرتّبة.",
  "inc": ["توليب أبيض صناعي", "حافة دانتيل ولولو", "مسكة مغطاة باللولو"]},
 {"n": "23", "slug": "jouri-ahmar", "style": "jouri", "name": "جوري أحمر بمقبض لولو",
  "lead": "جوري أحمر كثيف بإطار من الجبسوفيل الأبيض، ومسكة مغطاة باللولو. جريئة ورومانسية.",
  "inc": ["جوري أحمر صناعي عالي الجودة", "إطار جبسوفيل أبيض", "مسكة مغطاة باللولو"]},
 {"n": "24", "slug": "naem-lulu", "style": "khotoba", "name": "ألوان ناعمة باللولو",
  "lead": "توليب وجوري أبيض مع جربيرا خوخية وجبسوفيل زهري، وخيوط لولو. ألوان هادئة لفستان الخطوبة.",
  "inc": ["توليب وجوري أبيض", "جربيرا وجبسوفيل بألوان ناعمة", "خيوط لولو"]},
 {"n": "25", "slug": "peony-dantel", "style": "peony", "name": "بيوني أبيض بمقبض دانتيل",
  "lead": "بيوني أبيض كبير بتنسيق دائري ممتلئ، ومسكة ملفوفة بالدانتيل على سيقان خضراء. نعومة كاملة.",
  "inc": ["بيوني أبيض صناعي", "تنسيق دائري ممتلئ", "مسكة دانتيل"]},
]
KHOTOBA_SLUGS = ["zahri-naem", "naem-lulu", "kala-zahr-wardi", "kala-jouri-azraq"]
for c in CATALOG:
    c["img"] = "sowar/maska-" + c["n"] + ".webp"; c["w"], c["h"] = 900, 1200
    c["h1"] = "مسكة عروس " + c["name"]

_CAT_SLUGS = {c["slug"] for c in CATALOG}
for _m in MODELS:  # الموديلات القديمة اللي ما إلها صورة ستوديو: صفحاتها بتضل (روابط جوجل) بس مش بالكتالوج
    _m["img"] = "model-" + _m["slug"] + ".webp"; _m["legacy"] = True
MODELS = CATALOG + [m for m in MODELS if m["slug"] not in _CAT_SLUGS]
CAT_BY_N = {c["n"]: c for c in CATALOG}
def model_path(m): return MODELS_PATH + m["slug"] + "/"
def model_img(m): return m["img"]
def model_cards(items, eager=0):
    return "".join(f'''<li><a class="pcard" href="{model_path(m)}">
  <span class="pc-img">{img(m["img"], m["h1"] + " — هدايا سلمى", lazy=(i >= eager), w=m["w"], h=m["h"])}<em class="pc-sale">خصم {SALE_PCT}%</em></span>
  <b>{E(m["name"])}</b>
  <span class="pc-desc">{E(m["lead"])}</span>
  <span class="pc-price"><strong>{P['masaka']}</strong> دينار <s>{P['masaka_old']} دينار</s></span>
</a></li>''' for i, m in enumerate(items))
PEONY = ("sowar/maska-07.webp", "مسكة عروس بيوني أبيض باللولو", "بيوني أبيض باللولو")

# =====================================================================
# الأسئلة الشائعة — نفس صيغة سؤال الناس
# =====================================================================
FAQ = [
    ("من أين أشتري مسكة عروس في الأردن؟",
     f"من هدايا سلمى، حيث نجهّز مسكات العرائس من التوليب والكريستال والكالا والجوري والبيوني بسعر {P['masaka']} دينارًا، ونوصلها إلى جميع محافظات الأردن مقابل {DELIVERY} دينار. يتم الطلب برسالة على إنستغرام salma.gifts1."),
    ("كم سعر مسكة العروس؟",
     f"سعرها الحالي {P['masaka']} دينارًا لجميع الأنواع (عرض خاص، والسعر الأصلي {P['masaka_old']})، و{withdel('masaka')} دينارًا شاملة التوصيل."),
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
    ("أين أجد صينية دبل بالأسماء في الأردن؟",
     f"هدايا سلمى متجر أردني أونلاين يجهّز صواني الدبل والخطوبة من المرآة بظهر خشبي، بأسماء العروسين والتاريخ مع علبتين للخواتم، بسعر {P['saniya']} دينارًا، مع التوصيل إلى جميع محافظات الأردن خلال يومين والمعاينة والدفع عند الاستلام. اطلبوا برسالة على إنستغرام salma.gifts1."),
    ("هل تصلح الصينية للخطوبة ولكتب الكتاب؟",
     "نعم، تُستخدم لتلبيس الدبل في الخطوبة وفي عقد القران. ولكتب الكتاب يمكن طلبها ضمن بكج مع كتاب التوقيع والبصمات أو برواز البصمات."),
    ("أين أجد مسكات عرايس في الأردن؟",
     f"هدايا سلمى متجر أردني أونلاين يجهّز مسكات عرايس من الورد الصناعي عالي الجودة: توليب وكريستال وكالا وجوري وبيوني، بسعر {P['masaka']} دينارًا لكل الأنواع، مع التوصيل إلى جميع محافظات الأردن خلال يومين والمعاينة والدفع عند الاستلام. اطلبوا برسالة على إنستغرام salma.gifts1."),
]
FAQ += [
    ("وين ألاقي مسكة عروس بأقل من 20 دينار في الأردن؟",
     f"عند هدايا سلمى، سعر مسكة العروس حاليًا {P['masaka']} دينارًا (عرض خاص)، و{withdel('masaka')} دينارًا شاملة التوصيل إلى أي محافظة في الأردن. ورد صناعي عالي الجودة لا يذبل، من 20 إلى 25 وردة، مع معاينة ودفع عند الاستلام. الطلب برسالة على إنستغرام salma.gifts1."),
    ("مين عامل عروض على مسكات العرايس في الأردن؟",
     f"هدايا سلمى عندها عرض خاص على كل موديلات مسكات العرايس: {P['masaka']} دينارًا بدل {P['masaka_old']}، لكل الأنواع (توليب، كالا، جوري، بيوني، كريستال)، والتوصيل لكل المحافظات بـ{DELIVERY} دينار."),
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
    "name": "Salma Gifts - هدايا سلمى", "alternateName": ["هدايا سلمى", "Salma Gifts", "SalmaGifts", "Salma Gifts Jordan", "سلمى جيفتس", "سلمى للهدايا"],
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
    cur = lambda p: ' aria-current="page"' if p == path else ""
    def grp(title, links):
        return f'<p class="d-title">{title}</p>' + "".join(f'<a href="{h}"{cur(h)}>{E(t)}</a>' for t, h in links)
    drawer = (f'<div class="d-head"><span class="brand-name">هدايا سلمى</span><button class="d-close" type="button" aria-label="إغلاق القائمة">×</button></div>'
        + grp("مسكات العروس", [(s_["nav"], s_["path"]) for s_ in STYLES] + [("عرض جميع الموديلات", MODELS_PATH)])
        + grp("منتجاتنا الثانية", [(PAGES[k]["nav"], PAGES[k]["path"]) for k in ["sawani", "bakjat", "mahr", "grad"]])
        + grp("معلومات", [("الرئيسية", "/"), (PAGES["tawseel"]["nav"], PAGES["tawseel"]["path"]), (PAGES["faq"]["nav"], PAGES["faq"]["path"]), ("نصائح للعروس", MAQALAT_PATH)])
        + f'<div class="d-cta">{cta("احجزي على إنستغرام", "btn btn-primary btn-block", "cta_drawer")}</div>')
    tab = lambda h, t, ico: f'<a href="{h}"{cur(h)}>{ico}<span>{t}</span></a>'
    tabbar = ('<nav class="tabbar" aria-label="تنقل سريع">'
        + tab("/", "الرئيسية", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M3 11l9-7 9 7v9h-6v-6H9v6H3z"/></svg>')
        + tab(MODELS_PATH, "الموديلات", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="4" y="4" width="7" height="7" rx="2"/><rect x="13" y="4" width="7" height="7" rx="2"/><rect x="4" y="13" width="7" height="7" rx="2"/><rect x="13" y="13" width="7" height="7" rx="2"/></svg>')
        + f'<a class="tab-cta" href="{IG_DM}" target="_blank" rel="noopener" data-event="cta_tabbar"><span class="tab-ig">{IG_ICON}</span><span>احجزي</span></a>'
        + tab(PAGES["tawseel"]["path"], "الأسعار", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M20 12l-8 8-9-9V3h8z"/><circle cx="7.5" cy="7.5" r="1.5"/></svg>')
        + '<button class="tab-menu" type="button" aria-label="القائمة" aria-controls="mobile-nav"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h10"/></svg><span>القائمة</span></button>'
        + '</nav>')
    graph = [STORE, {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/",
                     "name": "هدايا سلمى - Salma Gifts", "inLanguage": "ar", "publisher": {"@id": STORE_ID}}]
    graph += [s for s in schemas if s]
    for g in graph:
        if g.get("@type") == "Product":
            g["offers"]["url"] = canonical
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    extra_preload = '\n<link rel="preload" href="/assets/fonts/amiri-700-arabic.woff2" as="font" type="font/woff2" crossorigin>' if key == "home" else ""
    ga = (f'\n<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>'
          f'\n<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","{GA_ID}");</script>') if GA_ID else ""
    if CLARITY_ID:
        ga += ('\n<script>(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};'
               't=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;'
               'y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})'
               f'(window,document,"clarity","script","{CLARITY_ID}");</script>')
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
<meta name="theme-color" content="#FAF5EF">
<meta name="p:domain_verify" content="10f3786eb5995c7295863fef211ec348"/>
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/aref-ruqaa-700-arabic.woff2" as="font" type="font/woff2" crossorigin>
{extra_preload}
<link rel="stylesheet" href="/assets/css/style.css?v={VERSION}">{ga}
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<a class="skip" href="#main">تخطَّ إلى المحتوى</a>

<header class="site-header">
  <div class="header-row">
    <button class="menu-btn" type="button" aria-label="القائمة" aria-expanded="false" aria-controls="mobile-nav">
      <span></span><span></span><span></span>
    </button>
    <a class="brand" href="/" aria-label="هدايا سلمى - الرئيسية">
      <img src="/assets/img/logo.webp" alt="شعار هدايا سلمى Salma Gifts" width="105" height="120">
      <span class="brand-text"><span class="brand-name">هدايا سلمى</span><span class="brand-en">SALMA GIFTS</span></span>
    </a>
    <nav class="main-nav" aria-label="القائمة الرئيسية">{nav}</nav>
    <a class="ig-btn" href="{IG}" target="_blank" rel="noopener" aria-label="إنستغرام هدايا سلمى">{IG_ICON}</a>
  </div>
</header>
<div class="drawer-veil" hidden></div>
<nav class="mobile-nav drawer" id="mobile-nav" aria-label="القائمة">{drawer}</nav>

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
      <li><a href="{MODELS_PATH}">جميع موديلات المسكات</a></li>
      <li><a href="{IG}" target="_blank" rel="noopener">إنستغرام: salma.gifts1</a></li>
      <li><a href="{FB}" target="_blank" rel="noopener">فيسبوك</a> · <a href="{MESSENGER}" target="_blank" rel="noopener">ماسنجر</a></li>
    </ul>
  </div>
  <p class="copy">© {datetime.date.today().year} Salma Gifts - هدايا سلمى (سلمى جيفتس)، الأردن</p>
</footer>

{tabbar}
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

SALE_PCT = round((P["masaka_old"] - P["masaka"]) * 100 / P["masaka_old"])
def price_line(k, note=None):
    note = note or f"{withdel(k)} دينارًا شاملة التوصيل إلى أي محافظة"
    if k == "masaka":
        return (f'<div class="p-price sale"><span class="pp-label">السعر الحالي</span>'
                f'<p class="pp-row"><b>{P[k]} <small>دينار</small></b><s class="was">{P["masaka_old"]} دينار</s><em class="offer">خصم {SALE_PCT}%</em></p>'
                f'<span>{E(note)}</span></div>')
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
<section class="section maker-sec sec-blush" id="asmaa">
  <div class="container hero-inner">
    <h2>جرّبي أسماءكم <span>قبل الحجز</span></h2>
    <p class="section-intro">اكتبي اسم العريس والعروس، وشوفيها على تعليقة المسكة أو على صينية الخطوبة.</p>

    <form class="maker" id="maker" action="{IG_DM}" target="_blank" novalidate>
      <div class="stage" data-mode="tag">
        <div class="tray" aria-hidden="true">
          <svg class="pearls" viewBox="0 0 200 200"><circle cx="100" cy="100" r="95.5"/><circle class="pearl-shine" cx="100" cy="100" r="95.5"/></svg>
          <div class="mirror">
            <p class="verse">وجعل بينكم مودة ورحمة</p>
            <div class="boxes"><span data-out="gi">{g[0]}</span><span data-out="bi">{b[0]}</span></div>
            <p class="names row"><span data-out="g">{kashida(g)}</span><span class="amp">♥</span><span data-out="b">{kashida(b)}</span></p>
            <p class="date" data-out="d">12.12.2026</p>
          </div>
          <svg class="pf" style="left:78.8%;top:18.0%;width:9%;transform:translate(-50%,-50%) rotate(-96deg)" viewBox="0 0 40 40" aria-hidden="true"><g><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(0 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(72 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(144 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(216 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(288 20 20)"/></g><circle class="c" cx="20" cy="20" r="5.2"/><circle class="h" cx="18.4" cy="18.4" r="1.6"/></svg><svg class="pf" style="left:88.0%;top:29.8%;width:11%;transform:translate(-50%,-50%) rotate(-56deg)" viewBox="0 0 40 40" aria-hidden="true"><g><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(0 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(72 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(144 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(216 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(288 20 20)"/></g><circle class="c" cx="20" cy="20" r="5.2"/><circle class="h" cx="18.4" cy="18.4" r="1.6"/></svg><svg class="pf" style="left:92.6%;top:44.0%;width:9%;transform:translate(-50%,-50%) rotate(-16deg)" viewBox="0 0 40 40" aria-hidden="true"><g><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(0 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(72 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(144 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(216 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(288 20 20)"/></g><circle class="c" cx="20" cy="20" r="5.2"/><circle class="h" cx="18.4" cy="18.4" r="1.6"/></svg><svg class="pf" style="left:92.1%;top:58.9%;width:11%;transform:translate(-50%,-50%) rotate(24deg)" viewBox="0 0 40 40" aria-hidden="true"><g><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(0 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(72 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(144 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(216 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(288 20 20)"/></g><circle class="c" cx="20" cy="20" r="5.2"/><circle class="h" cx="18.4" cy="18.4" r="1.6"/></svg><svg class="pf" style="left:86.5%;top:72.8%;width:9%;transform:translate(-50%,-50%) rotate(64deg)" viewBox="0 0 40 40" aria-hidden="true"><g><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(0 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(72 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(144 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(216 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(288 20 20)"/></g><circle class="c" cx="20" cy="20" r="5.2"/><circle class="h" cx="18.4" cy="18.4" r="1.6"/></svg><svg class="pf" style="left:9.6%;top:64.7%;width:8%;transform:translate(-50%,-50%) rotate(320deg)" viewBox="0 0 40 40" aria-hidden="true"><g><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(0 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(72 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(144 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(216 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(288 20 20)"/></g><circle class="c" cx="20" cy="20" r="5.2"/><circle class="h" cx="18.4" cy="18.4" r="1.6"/></svg><svg class="pf" style="left:7.0%;top:51.5%;width:10%;transform:translate(-50%,-50%) rotate(356deg)" viewBox="0 0 40 40" aria-hidden="true"><g><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(0 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(72 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(144 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(216 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(288 20 20)"/></g><circle class="c" cx="20" cy="20" r="5.2"/><circle class="h" cx="18.4" cy="18.4" r="1.6"/></svg><svg class="pf" style="left:8.7%;top:38.1%;width:8%;transform:translate(-50%,-50%) rotate(392deg)" viewBox="0 0 40 40" aria-hidden="true"><g><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(0 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(72 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(144 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(216 20 20)"/><ellipse cx="20" cy="9.5" rx="7" ry="10" transform="rotate(288 20 20)"/></g><circle class="c" cx="20" cy="20" r="5.2"/><circle class="h" cx="18.4" cy="18.4" r="1.6"/></svg>
        </div>
        <div class="tag-scene" aria-hidden="true">
          {img("sowar/maska-05.webp", "مسكة عروس كالا أبيض", w=900, h=1200)}
          <div class="tag">
            <p class="names"><span data-out="g">{kashida(g)}</span><span class="amp">♥</span><span data-out="b">{kashida(b)}</span></p>
            <p class="date" data-out="d">12.12.2026</p>
          </div>
        </div>
        <a class="real-inset" href="/sawani-khotoba/" aria-label="شاهدوا صواني الخطوبة الحقيقية">{img("saniyet-khotoba-real.webp", "صينية دبل خطوبة حقيقية من طلبات هدايا سلمى بالأسماء والتاريخ وعلب الخواتم", w=600, h=600)}<span class="cap">صينية حقيقية من طلباتنا</span></a>
      </div>

      <div class="fields">
        <label class="field"><span>اسم العريس</span><input name="groom" autocomplete="off" maxlength="16" placeholder="{g}" inputmode="text"></label>
        <label class="field"><span>اسم العروس</span><input name="bride" autocomplete="off" maxlength="16" placeholder="{b}" inputmode="text"></label>
      </div>

      <fieldset class="choice">
        <legend class="sr">ماذا تريدون بهذه الأسماء؟</legend>
        <label><input type="radio" name="item" value="tag" checked data-price="" data-label="مسكة عروس مع تعليقة"><span>تعليقة المسكة</span></label>
        <label><input type="radio" name="item" value="tray" data-price="{P['saniya']}" data-label="صينية خطوبة بالأسماء"><span>صينية الخطوبة</span></label>
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

STAR = '<svg class="star7" viewBox="0 0 24 24" aria-hidden="true"><polygon points="12.00,2.00 14.00,7.86 19.82,5.77 16.48,10.98 21.75,14.23 15.60,14.87 16.34,21.01 12.00,16.60 7.66,21.01 8.40,14.87 2.25,14.23 7.52,10.98 4.18,5.77 10.00,7.86"/></svg>'
STATS = [("+1500", "طلب جهّزناه"), ("+25", "موديل مسكة"), ("12", "محافظة نوصل لها")]

def build_home():
    names = dict(SOWAR)
    hero = f"""
<section class="hx">
  {img("sowar/maska-17.webp", "مسكة عروس توليب باللولو والكريستال — هدايا سلمى، الأردن", lazy=False, w=900, h=1200)}
  <div class="hx-in">
    <p class="hx-pill">{STAR}<span>أول موقع أردني مختص بمسكات العرايس</span>{STAR}</p>
    <h1><span class="hx-t">مسكات عروس 2026</span><span class="hx-s">مسكتك جاهزة باسمك وتاريخك، ورد صناعي فاخر لا يذبل</span></h1>
    <div class="hx-bot">
      <p class="hx-price"><span class="hx-sale">خصم {SALE_PCT}%</span><b>{P['masaka']}</b><em>دينار</em><s>{P['masaka_old']}</s></p>
      <div class="hx-btns">
        <a class="btn btn-light" href="#mawdeelat" data-event="cta_hero_models">اختاري مسكتك</a>
        {cta("احجزي بالإنستغرام", "btn btn-glass", "cta_hero")}
      </div>
    </div>
  </div>
</section>
<div class="stats container">{"".join(f'<div><b data-count="{n.lstrip("+")}" data-prefix="{"+" if n.startswith("+") else ""}">{n}</b><span>{t}</span></div>' for n, t in STATS)}</div>"""
    types = [(STYLES[0], "08"), (STYLES[2], "11"), (STYLES[3], "01"), (next(x for x in STYLES if x["key"] == "khotoba"), "24")]
    type_html = "".join(f'<li><a href="{st["path"]}"><i>{img("sowar/maska-" + n + ".webp", st["nav"] + " من هدايا سلمى", w=900, h=1200)}</i><span>{E("مسكات خطوبة" if st["key"] == "khotoba" else st["name"])}</span></a></li>' for st, n in types)
    best = [CAT_BY_N[n] for n in ["02", "07", "08", "21", "23", "01", "03", "25"]]
    best_html = model_cards(best)
    others = [
        (PAGES["sawani"]["path"], "صواني الخطوبة والدبل", "مرآة بأسمائكم وعلب الخواتم", "saniya", "saniyet-khotoba-1.webp"),
        (PAGES["bakjat"]["path"], "بكجات كتب الكتاب", "صينية وكتاب توقيع وبصمات", "bakj_berwaz", "bakj-katb-ktab-2.webp"),
        (PAGES["mahr"]["path"], "صندوق المهر", "لتقديم المهر للعروس", "mahr", "sandouq-mahr-1.webp"),
        (PAGES["grad"]["path"], "هدايا التخرج", "باسم الخريج والتخصص", "takharroj", "hadiyet-takharroj-1.webp"),
    ]
    others_html = "".join(f"""<li><a href="{h}">{img(im, t + " من هدايا سلمى", w=720, h=900)}<span class="oc-t"><b>{E(t)}</b><span>{E(d)}</span><em>من {P[k]} دينار</em></span></a></li>""" for h, t, d, k, im in others)
    steps = [("اختاري المسكة", "تصفّحي الموديلات وأرسلي لنا صورة المسكة على إنستغرام."),
             ("أرسلي تاريخ المناسبة", "ولون الفستان إن أردتِ، وحدّدي يوم التوصيل."),
             ("استلمي وعايني قبل الدفع", f"توصيل لكل المحافظات بـ{DELIVERY} دينار خلال يومين.")]
    st = "".join(f'<li><b>{t}</b><span>{d}</span></li>' for t, d in steps)
    trust = [("معاينة قبل الدفع", "والدفع عند الاستلام نقدًا أو كليك", '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="m9 12 2 2 4-4"/>'),
             ("توصيل خلال يومين", "إلى جميع محافظات الأردن", '<path d="M3 7h11v9H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/>'),
             ("ورد لا يذبل", "تبقى المسكة ذكرى بعد المناسبة", '<path d="M12 21s-7-4.5-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 5.5-7 10-7 10z"/>'),
             ("كل قطعة على حدة", "بأسمائكم ونراجعها قبل أن تخرج", '<path d="M4 20h16M6 16l3-9 3 5 3-7 3 11"/>')]
    trust_html = "".join(f'<li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">{ic}</svg><b>{t}</b><span>{d}</span></li>' for t, d, ic in trust)
    faqs = [FAQ[17], FAQ[18], FAQ[1], FAQ[19], FAQ[2], FAQ[14], FAQ[9]]
    body = hero + f"""
<section class="section" id="anwaa"><div class="container">
  <p class="kicker">ابدئي من هنا</p>
  <div class="section-head"><h2>تسوّقي حسب النوع</h2><a href="{PAGES['masakat']['path']}">كل المسكات {ARROW}</a></div>
  <ul class="types">{type_html}</ul>
</div></section>

<section class="section" id="mawdeelat"><div class="container">
  <p class="kicker">مجموعة 2026</p>
  <div class="section-head"><h2>الأكثر طلبًا</h2><a href="{MODELS_PATH}">جميع الموديلات {ARROW}</a></div>
  <p class="section-intro">ورد صناعي فاخر لا يذبل، ونجهّز أي موديل بلون يناسب فستانك.</p>
  <ul class="pgrid">{best_html}</ul>
  <p class="center"><a class="btn btn-primary" href="{MODELS_PATH}">عرض جميع الموديلات</a></p>
</div></section>

""" + name_preview() + f"""
<section class="section sec-sage"><div class="container">
  <p class="kicker">للخطوبة وكتب الكتاب</p>
  <div class="section-head"><h2>منتجاتنا الثانية</h2><a href="{PAGES['tawseel']['path']}">كل الأسعار {ARROW}</a></div>
  <ul class="others">{others_html}</ul>
</div></section>

<section class="section"><div class="container">
  <h2>كيف تطلبين مسكتك؟</h2>
  <ol class="steps">{st}</ol>
</div></section>

<section class="section sec-cocoa"><div class="container">
  <p class="kicker">ثقة أكثر من 1500 عروس</p>
  <h2>لماذا هدايا سلمى؟</h2>
  <p class="section-intro">أنجزنا أكثر من 1500 طلب، وكل طلب يُجهَّز في ورشتنا على حدة كأنه الوحيد.</p>
  <ul class="trust">{trust_html}</ul>
</div></section>
""" + articles_block() + f"""
<section class="section"><div class="container narrow">
  <div class="section-head"><h2>أسئلة متكررة</h2><a href="{PAGES['faq']['path']}">كل الأسئلة {ARROW}</a></div>
  {faq_html(faqs)}
</div></section>
"""
    title = f"مسكات عروس 2026 في الأردن بـ{P['masaka']} دينار: مسكة عروس بصور حقيقية | هدايا سلمى"
    desc = f"مسكات عروس 2026 (مسكات عرايس) ورد صناعي لا يذبل بـ{P['masaka']} دينار: توليب، كالا، جوري ومسكات خطوبة. أكثر من 1500 طلب، وصواني خطوبة بالأسماء {P['saniya']} دينار. معاينة ودفع عند الاستلام وتوصيل لكل محافظات الأردن."
    write("/", layout("home", "/", title, desc, body, [faq_schema(faqs)], og_img="sowar/maska-02.webp"))

# =====================================================================
# مسكات العروس (الصفحة الرئيسية للمسكات)
# =====================================================================
def build_masakat():
    head, bsch = page_intro([(PAGES["masakat"]["nav"], PAGES["masakat"]["path"])],
        "مسكات عروس 2026 في الأردن",
        "مسكات عروس ومسكات عرايس (مسكة العروس) من ورد صناعي عالي الجودة لا يذبل، من 20 إلى 25 وردة: توليب، كريستال، كالا، جوري وبيوني، وبأي لون يناسب فستانكم.",
        "masaka")
    cards = "".join(f"""<li><a href="{s['path']}">{img(s['photos'][0][0], s['photos'][0][1])}<span class="label"><b>{E(s['nav'])}</b><span>{P['masaka']} دينار</span></span></a></li>""" for s in STYLES)
    faqs = [FAQ[17], FAQ[18], FAQ[19], FAQ[0], FAQ[1], FAQ[13], FAQ[14], FAQ[2], FAQ[7], FAQ[9]]
    body = head + f"""
<section class="section"><div class="container">
  <h2>أنواع مسكات العروس</h2>
  <p class="section-intro">كل الأنواع بسعر واحد. وإن أعجبكم تصميم غير موجود هنا، أرسلوا لنا صورته.</p>
  <ul class="rail rail-grid">{cards}</ul>
</div></section>

<section class="section tint"><div class="container">
  <h2>موديلات المسكات بصور حقيقية</h2>
  <p class="section-intro">كل موديل بصفحة فيها صورته وتفاصيله. اختاروا وأرسلوا لنا اسم الموديل.</p>
  <ul class="pgrid">{model_cards(CATALOG)}</ul>
  <p><a class="btn btn-quiet" href="{SOWAR_PATH}">شوفي صور مسكات عروس 2026</a></p>
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


<section class="section"><div class="container narrow">
  <h2>أكثر مسكات العروس طلبًا في 2026</h2>
  <p>العرايس بيسألونا أكثر شي عن: <strong>مسكة عروس توليب أبيض</strong> (<a href="{STYLES[0]['path']}">موديلات التوليب</a>)، <strong>مسكة عروس كريستال</strong>، <strong>مسكة عروس كالا</strong>، <strong>مسكة عروس جوري</strong>، و<strong>مسكة عروس بيوني</strong>. ومنها الناعمة للخطوبة وكتب الكتاب، والفخمة والملكية للزفاف، ومسكات عروس للحنّة بألوان.</p>
  <p>وكلها ورد صناعي عالي الجودة شكله طبيعي وما بيذبل، بسعر واحد {P['masaka']} دينار بدل 25 (عرض خاص)، و{withdel('masaka')} مع التوصيل لعمّان والزرقاء وإربد والسلط ومادبا وجرش وعجلون والكرك والعقبة وكل محافظات الأردن.</p>
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
        f"مسكات عروس 2026 في الأردن: مسكة عروس بـ{P['masaka']} دينار | هدايا سلمى",
        f"مسكات عروس 2026 ومسكات عرايس في الأردن: مسكة عروس توليب أبيض وكريستال وكالا وجوري وبيوني، ورد صناعي لا يذبل، {P['masaka']} دينار و{withdel('masaka')} مع التوصيل لكل محافظات الأردن. معاينة ودفع عند الاستلام.",
        body, sch, og_img="masaka-arous-crystal.webp"))

def build_style(s):
    trail = [(PAGES["masakat"]["nav"], PAGES["masakat"]["path"]), (s["nav"], s["path"])]
    head, bsch = page_intro(trail, s["h1"], s["lead"], "masaka")
    faqs = [(q, a or f"سعرها {P['masaka']} دينارًا، و{withdel('masaka')} دينارًا شاملة التوصيل إلى أي محافظة.")
            for q, a in s["faq"]] + [FAQ[7], FAQ[9], FAQ[6]]
    others = "".join(f'<a href="{o["path"]}">{E(o["nav"])}</a>' for o in STYLES if o is not s)
    paras = "".join(f"<p>{E(p)}</p>" for p in s["about"])
    mine = [m for m in CATALOG if (m["slug"] in KHOTOBA_SLUGS if s["key"] == "khotoba" else m["style"] == s["key"])]
    models_block = (f'''<section class="section tint"><div class="container">
  <h2>موديلات مسكة ال{E(s['name'])}</h2>
  <ul class="pgrid">{model_cards(mine)}</ul>
  <p class="center"><a class="btn btn-primary" href="{MODELS_PATH}">عرض جميع الموديلات</a></p>
</div></section>
''') if mine else ""
    body = head + f"""
<section class="section flush"><div class="container">{mosaic(s["photos"])}</div></section>
<section class="section"><div class="container narrow">
  <h2>عن مسكة ال{E(s['name'])}</h2>
  {paras}
  {promise_list()}
</div></section>
{models_block}<section class="section"><div class="container narrow">
  <h2>أسئلة عن مسكة ال{E(s['name'])}</h2>
  {faq_html(faqs)}
  {('<p><a class="text-link" href="' + MAQALAT_PATH + {"khotoba": "maskat-khotoba-2026/", "tulip": "maskat-arous-tulip/"}.get(s["key"], "ajmal-maskat-arous-2026/") + '">' + {"khotoba": "أفكار مسكات خطوبة 2026", "tulip": "مسكة عروس توليب: أشكالها وسعرها"}.get(s["key"], "أجمل مسكات عروس 2026") + ' ' + ARROW + '</a></p>')}
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
        "صواني دبل وخطوبة بالأسماء في الأردن",
        "صينية دبل من المرآة تحمل أسماءكم وتاريخ المناسبة، بظهر خشبي يحميها من الكسر، مع علبتين للخواتم بحروفكم الأولى، ولؤلؤ ودانتيل.",
        "saniya", extra=f'<p><a class="text-link" href="/#maker">جرّبوا أسماءكم على الصينية {ARROW}</a></p>')
    faqs = [FAQ[15], FAQ[3], FAQ[16], FAQ[5], FAQ[6], FAQ[7], FAQ[9]]
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
  <h2>كيف نكتب أسماءكم على الصينية</h2>
  <p>نكتب اسم العريس أولًا ثم اسم العروس بخط عربي ممدود (بالكشيدة)، وتحتهما تاريخ المناسبة، وفوقهما الآية الكريمة. وإن رغبتم في عبارة بدلًا من الآية نكتبها لكم. وعلى علبتي الخواتم الحرف الأول من كل اسم.</p>
  <p>أرسلوا لنا الأسماء كما تريدون كتابتها بالضبط، والتاريخ، والعبارة إن وُجدت، ونحن نجهّز الصينية ونوصلها خلال يومين إلى أي محافظة.</p>
  <p><a class="text-link" href="/#maker">شاهدوا أسماءكم على الصينية قبل الطلب {ARROW}</a></p>
</div></section>
<section class="section"><div class="container narrow">
  <h2>هل تريدون الصينية مع كتاب عقد القران؟</h2>
  <p>اطلبوها ضمن بكج: بكج البرواز بسعر {P['bakj_berwaz']} دينارًا، أو البكج الأساسي بسعر {P['bakj_asasi']} دينارًا مع كتاب التوقيع والبصمات ورسالة العمر.</p>
  <p><a class="btn btn-quiet" href="{PAGES['bakjat']['path']}">تصفّحوا البكجات</a></p>
</div></section>
<section class="section tint"><div class="container narrow">
  <h2>أسئلة عن صواني الدبل والخطوبة</h2>
  {faq_html(faqs)}
  {related("sawani")}
</div></section>"""
    sch = [bsch, faq_schema(faqs),
           product_schema("صينية الخطوبة والدبل", "صينية من المرآة بظهر خشبي، بأسماء العروسين والتاريخ مع علبتين للخواتم ولؤلؤ ودانتيل.",
                          ["saniyet-khotoba-1.webp", "saniyet-khotoba-2.webp", "saniyet-khotoba-3.webp"], P["saniya"], sku="saniya")]
    write(PAGES["sawani"]["path"], layout("sawani", PAGES["sawani"]["path"],
        f"صواني دبل وخطوبة بالأسماء في الأردن بـ{P['saniya']} دينار | هدايا سلمى",
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
    adds = [("ستاند أسود", "stand"), ("قصاصات", "qassasat"), ("فناجين", "fanajin"), ("قصاصة التقويم أو رسالة العمر", "taqweem")]
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
def build_models_index():
    trail = [(PAGES["masakat"]["nav"], PAGES["masakat"]["path"]), ("جميع الموديلات", MODELS_PATH)]
    bc, bsch = breadcrumb(trail)
    chips = "".join(f'<a href="{x["path"]}">{E("مسكات خطوبة" if x["key"] == "khotoba" else x["name"])}</a>' for x in STYLES)
    body = bc + f"""
<section class="p-head container">
  <h1>جميع موديلات مسكات العروس</h1>
  <p class="lead">{len(CATALOG)} موديلًا بصور حقيقية، كلها ورد صناعي عالي الجودة لا يذبل، ونجهّز أي موديل بلون يناسب فستانك.</p>
  <div class="chips">{chips}</div>
</section>
<section class="section flush"><div class="container">
  <ul class="pgrid">{model_cards(CATALOG, eager=2)}</ul>
</div></section>
{section("قبل الحجز", promise_list(), cls="tint")}
<section class="section"><div class="container narrow">
  <h2>أسئلة عن موديلات المسكات</h2>
  {faq_html([FAQ[13], FAQ[1], FAQ[14], FAQ[7]])}
  {related("masakat")}
</div></section>"""
    itemlist = {"@type": "ItemList", "name": "موديلات مسكات العرايس — هدايا سلمى", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": SITE + model_path(m), "name": m["h1"]} for i, m in enumerate(CATALOG)]}
    sch = [bsch, itemlist, faq_schema([FAQ[13], FAQ[1], FAQ[14], FAQ[7]])]
    write(MODELS_PATH, layout("style-models", MODELS_PATH,
        f"موديلات مسكات عروس 2026: {len(CATALOG)} موديل بصور حقيقية بـ{P['masaka']} دينار | هدايا سلمى",
        f"جميع موديلات مسكات العروس 2026 بصور حقيقية: توليب، كالا، جوري، بيوني وكريستال باللولو والدانتيل. كل الموديلات {P['masaka']} دينار مع توصيل لكل الأردن.",
        body, sch, og_img=CATALOG[1]["img"]))

def build_model(m):
    st = next((x for x in STYLES if x["key"] == m["style"]), None)
    if st is None:
        st = {"path": PAGES["masakat"]["path"] + ("#peony" if m["style"] == "peony" else ""),
              "nav": "مسكة عروس بيوني" if m["style"] == "peony" else "مسكات العروس"}
    trail = [(PAGES["masakat"]["nav"], PAGES["masakat"]["path"]), ("جميع الموديلات", MODELS_PATH), (m["name"], model_path(m))]
    bc, bsch = breadcrumb(trail)
    faqs = [(f"كم سعر {m['h1']}؟", f"سعرها {P['masaka']} دينارًا، و{withdel('masaka')} دينارًا شاملة التوصيل إلى أي محافظة في الأردن."),
            ("هل يمكن تغيير لون الموديل؟", "نعم، نجهّز الموديل نفسه بلون يناسب فستانكم، للزفاف أو الخطوبة أو الحنّة أو كتب الكتاب. أرسلوا لنا اللون مع الطلب."),
            ("كيف أطلب هذا الموديل؟", f"أرسلوا لنا صورة المسكة برسالة على إنستغرام salma.gifts1، مع تاريخ المناسبة، ونؤكد لكم الطلب."),
            FAQ[7], FAQ[9]]
    pool = [x for x in CATALOG if x is not m]
    others = ([x for x in pool if x["style"] == m["style"]] + [x for x in pool if x["style"] != m["style"]])[:4]
    body = bc + f"""
<section class="pd container">
  <figure class="pd-img">{img(m["img"], m["h1"] + " — صورة حقيقية من هدايا سلمى", lazy=False, w=m["w"], h=m["h"])}</figure>
  <div class="pd-info">
    <h1>{E(m["h1"])}</h1>
    {price_line("masaka")}
    <p class="lead">{E(m["lead"])}</p>
    <div class="actions">{cta("احجزي هذه المسكة", "btn btn-primary btn-block", "cta_product")}</div>
    <h2 class="pd-h">تفاصيل المسكة</h2>
    {includes(m["inc"] + ["ورد صناعي عالي الجودة لا يذبل", "نجهّزها بلون يناسب فستانك"])}
    <p><a class="text-link" href="{st['path']}">كل أنواع {E(st['nav'])} {ARROW}</a></p>
  </div>
</section>
{section("قبل الحجز", promise_list(), cls="tint")}
<section class="section"><div class="container">
  <h2>قد يعجبك أيضًا</h2>
  <ul class="pgrid">{model_cards(others)}</ul>
  <p class="center"><a class="btn btn-primary" href="{MODELS_PATH}">عرض جميع الموديلات</a></p>
</div></section>
<section class="section"><div class="container narrow">
  <h2>أسئلة عن هذه المسكة</h2>
  {faq_html(faqs)}
</div></section>"""
    sch = [bsch, faq_schema(faqs),
           product_schema(m["h1"], m["lead"], [m["img"]], P["masaka"], sku="masaka-" + m["slug"])]
    write(model_path(m), layout("style-model", model_path(m),
        f"{m['h1']} بـ{P['masaka']} دينار | هدايا سلمى، الأردن",
        f"{m['h1']}: {m['lead']} {P['masaka']} دينار و{withdel('masaka')} مع التوصيل لكل محافظات الأردن، معاينة ودفع عند الاستلام.",
        body, sch, og_img=m["img"]))

# =====================================================================
# مقالات للعروس — بتجاوب على أسئلة بتنبحث (وبتربط على الموديلات)
# =====================================================================
MAQALAT_PATH = "/maqalat/"
def M(slug): return next(m for m in MODELS if m["slug"] == slug)
def mlink(slug):
    m = M(slug)
    return f'<a href="{model_path(m)}">{E(m["name"])}</a>'

def _art_dress():
    groups = [
        ("فستان منفوش (برنسيس)", "مسكة دائرية ممتلئة توازن حجم الفستان. المسكة الصغيرة تضيع أمام الفستان المنفوش.", ["jouri-abyad", "toulib-lulu", "kala-toulib-crystal"]),
        ("فستان ضيق أو حورية (ميرميد)", "مسكة منسدلة طويلة تكمّل خط الفستان من فوق لتحت.", ["turkish-qaws", "qaws-toulib", "kala-classic-strass"]),
        ("فستان ساتان بسيط بدون تطريز", "مسكة بخطوط نظيفة وبدون تفاصيل كثيرة، فالبساطة هنا هي الفخامة.", ["toulib-classic", "kala-classic-strass", "kala-gypsophila"]),
        ("فستان دانتيل أو ستايل بوهو", "مسكة ناعمة فيها جبسوفيل أو بيوني، تشبه نعومة الدانتيل.", ["peony-boho", "toulib-gypsophila", "jouri-zahri-toulib"]),
        ("فستان مطرّز بالكريستال أو لامع", "مسكة فيها كريستال أو ستراس، حتى تكون اللمعة متناسقة بين الفستان والمسكة.", ["toulib-crystal", "kala-toulib-crystal", "toulib-lulu"]),
        ("فستان خطوبة أو حنّة ملوّن", "هنا المسكة الملوّنة أجمل من البيضاء، أو مسكة بيضاء فيها لمسة من لون الفستان.", ["kala-jouri-azraq", "zahri-naem", "kala-zahr-wardi"]),
    ]
    blocks = "".join(f"<h3>{E(t)}</h3>\n<p>{E(d)} موديلات مناسبة: " + "، ".join(mlink(x) for x in xs) + ".</p>" for t, d, xs in groups)
    picks = [M(x) for x in ["jouri-abyad", "turkish-qaws", "toulib-classic", "peony-boho", "toulib-crystal", "kala-jouri-azraq"]]
    return f"""
<p>المسكة تظهر في كل صورة من صور يومك، فاختيارها مهم مثل اختيار الفستان. وأسهل طريقة للاختيار أن تبدئي من الفستان نفسه: قَصّته، وتفاصيله، ولونه.</p>
<h2>ثلاثة أسئلة قبل أن تختاري</h2>
<ol>
<li><b>ما قَصّة الفستان؟</b> منفوش، ضيق، أو بسيط. القصّة تحدد شكل المسكة: دائرية أو منسدلة أو بسيطة.</li>
<li><b>ما تفاصيل الفستان؟</b> دانتيل، كريستال، أو ساتان سادة. التفاصيل تحدد الإكسسوارات: لولو، كريستال، جبسوفيل، أو بدون.</li>
<li><b>ما المناسبة؟</b> الزفاف غالبًا بالأبيض، أما الخطوبة والحنّة وكتب الكتاب فتحتمل الألوان.</li>
</ol>
<h2>المسكة المناسبة لكل نوع فستان</h2>
{blocks}
<h2>اللون: أبيض مع أبيض؟</h2>
<p>الأبيض درجات: أبيض ناصع، وأوف وايت، وعاجي. إذا كان فستانك أوف وايت، فمسكة بورد أبيض دافئ أو مع جبسوفيل تكون متناسقة أكثر. ونجهّز أي موديل باللون الذي يناسب فستانك.</p>
<h2>الحجم حسب طولك</h2>
<p>العروس الناعمة أو القصيرة تناسبها مسكة متوسطة الحجم حتى لا تغطيها. والعروس الطويلة تحتمل المسكة المنسدلة على شكل قوس.</p>
<h2>المسكة بعد المناسبة</h2>
<p>إذا كانت المسكة من ورد صناعي عالي الجودة، فهي لا تذبل وتبقى ذكرى في البيت.</p>
<p>إذا ما عرفتي أي موديل يناسبك، أرسلي لنا صورة الفستان برسالة على إنستغرام ونساعدك تختاري.</p>
<ul class="rail rail-grid">{model_cards(picks)}</ul>"""

def _art_tulip_calla():
    tul = [m for m in CATALOG if m["style"] in ("tulip", "crystal")][:6]
    cal = [m for m in CATALOG if m["style"] == "calla"][:6]
    rows = [("الشكل", "وردة على شكل كأس مغلق، ناعمة ودائرية", "وردة طويلة على شكل قمع، بخطوط نظيفة"),
            ("الإحساس", "رقيقة وأنثوية وعصرية", "أنيقة وكلاسيكية وفخمة"),
            ("الفستان المناسب", "المنفوش والدانتيل والبوهو", "الضيق والحورية والساتان البسيط"),
            ("شكل المسكة", "دائرية ممتلئة، أو منسدلة كالقوس", "طويلة بسيقان ظاهرة، أو منسدلة"),
            ("مع الإكسسوارات", "تبرز مع اللولو والكريستال والتول", "تبرز مع الستراس والجبسوفيل"),
            ("عدد الموديلات عندنا", f"{len(tul)} موديلات", f"{len(cal)} موديلات"),
            ("السعر عندنا", f"{P['masaka']} دينار", f"{P['masaka']} دينار")]
    tr = "".join(f"<tr><th>{a}</th><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows)
    return f"""
<p>التوليب والكالا أكثر نوعين تسأل عنهما العرايس. الاثنان جميلان، والفرق بينهما في الشكل والإحساس، لا في الجودة.</p>
<h2>الفرق باختصار</h2>
<div class="table-wrap"><table class="cmp"><thead><tr><th></th><th>توليب</th><th>كالا</th></tr></thead><tbody>{tr}</tbody></table></div>
<h2>اختاري التوليب إذا…</h2>
<ul><li>فستانك منفوش أو فيه دانتيل.</li><li>تحبين المسكة الناعمة الدائرية.</li><li>تريدين لولو أو كريستال حول الورد.</li></ul>
<h2>اختاري الكالا إذا…</h2>
<ul><li>فستانك ضيق أو ساتان بسيط.</li><li>تحبين المسكة الطويلة ذات الخطوط النظيفة.</li><li>تريدين مسكة منسدلة لافتة مثل {mlink("turkish-qaws")}.</li></ul>
<h2>ولو حابة الاثنين؟</h2>
<p>في موديلات تجمعهما: {mlink("kala-toulib-crystal")}، و{mlink("jouri-zahri-toulib")} وفيه توليب وكالا حول الجوري.</p>
<h2>موديلات التوليب</h2>
<ul class="rail rail-grid">{model_cards(tul)}</ul>
<h2>موديلات الكالا</h2>
<ul class="rail rail-grid">{model_cards(cal)}</ul>"""

def _art_price():
    return f"""
<p>سعر مسكة العروس في الأردن يختلف كثيرًا من محل لمحل، وأكثر شيء يؤثر عليه هو نوع الورد: طبيعي أو صناعي. هذه الأشياء التي تحدد السعر، وكيف تقارنين قبل أن تحجزي.</p>
<h2>ما الذي يحدد سعر المسكة؟</h2>
<ol>
<li><b>طبيعي أو صناعي:</b> الورد الطبيعي يُجهَّز يوم المناسبة ويذبل بعدها بأيام، وسعره يتغير حسب الموسم. الصناعي عالي الجودة يُجهَّز مسبقًا ويبقى ذكرى.</li>
<li><b>عدد الورد وحجم المسكة:</b> المسكة الممتلئة أو المنسدلة تحتاج وردًا أكثر.</li>
<li><b>الإكسسوارات:</b> اللولو، والكريستال، والستراس على المسكة، والتول والدانتيل.</li>
<li><b>التوصيل:</b> هل السعر شامل التوصيل لمحافظتك أم لا.</li>
</ol>
<h2>سعر مسكة العروس عند هدايا سلمى</h2>
<div class="table-wrap"><table class="cmp"><tbody>
<tr><th>المسكة، كل الموديلات ({len(CATALOG)} موديل)</th><td>{P['masaka']} دينار (عرض خاص، السعر الأصلي {P['masaka_old']})</td></tr>
<tr><th>مع التوصيل لأي محافظة</th><td>{withdel('masaka')} دينار</td></tr>
</tbody></table></div>
<p>ورد صناعي عالي الجودة لا يذبل، من 20 إلى 25 وردة، وبأي لون يناسب الفستان. السعر واحد سواء كانت المسكة توليب أو كالا أو جوري أو بيوني أو كريستال.</p>
<h2>قبل أن تحجزي من أي مكان، تأكدي من:</h2>
<ul>
<li><b>صور حقيقية</b> من شغلهم، لا صور من الإنترنت.</li>
<li><b>المعاينة قبل الدفع</b>، والدفع عند الاستلام.</li>
<li><b>مدة التجهيز</b>، واحجزي قبل المناسبة بثلاثة أيام على الأقل.</li>
<li><b>السعر النهائي</b> مع التوصيل والإضافات.</li>
</ul>
<p><a class="btn btn-quiet" href="{MODELS_PATH}">عرض جميع الموديلات</a></p>"""


def _cat(slugs): return [m for m in CATALOG if m["slug"] in slugs]

def _art_best2026():
    groups = [
        ("التوليب الأبيض باللولو والكريستال", "الأكثر طلبًا هذا الموسم: توليب أبيض ناعم يحيط به إطار من اللولو أو حبّات الكريستال، ومسكة ستراس أو لولو. يليق بالفستان المنفوش والمطرّز.", ["toulib-crystal", "toulib-lulu", "toulib-lulu-crystal"]),
        ("الكالا الطويلة الأنيقة", "خطوط الكالا الطويلة تعطي إطلالة ملكية هادئة، وتناسب الفستان الضيق والساتان. أجملها مع مقبض ستراس أو دانتيل.", ["kala-classic-strass", "kala-abyad", "kala-dantel"]),
        ("البيوني الممتلئ", "زهور كبيرة ومفتوحة بتنسيق دائري، ناعمة جدًا في الصور، وتناسب ستايل البوهو والدانتيل.", ["peony-lulu", "peony-dantel"]),
        ("المسكة المنسدلة (القوس)", "توليب ينسدل على شكل قوس مع خيوط اللولو، لعروس تحب التصميم المختلف، وتناسب فستان الحورية.", ["qaws-toulib", "toulib-halaqa-lulu"]),
        ("لمسة لون للخطوبة والحنّة", "الأزرق الفاتح، والزهري، والخوخي: ألوان هادئة تكمّل فستان الخطوبة أو الحنّة.", ["kala-jouri-azraq", "kala-zahr-wardi", "zahri-naem"]),
        ("الجوري الكلاسيكي", "الجوري الأبيض مع الجبسوفيل لا يخرج من الموضة، والأحمر لعروس جريئة ورومانسية.", ["jouri-abyad", "jouri-ahmar"]),
    ]
    blocks = "".join(f"<h2>{i}. {E(t)}</h2>\n<p>{E(d)}</p>\n<ul class=\"pgrid\">{model_cards(_cat(xs))}</ul>" for i, (t, d, xs) in enumerate(groups, 1))
    return f"""
<p>هذه أجمل مسكات العروس لموسم 2026 في الأردن، بصور حقيقية من شغلنا. كلها ورد صناعي عالي الجودة لا يذبل، فتبقى المسكة ذكرى بعد العرس، ونجهّز أي موديل بلون يناسب فستانك.</p>
{blocks}
<h2>كيف تختارين بين هذه الأفكار؟</h2>
<p>ابدئي من الفستان: المنفوش تناسبه المسكة الدائرية الممتلئة، والضيق تناسبه المنسدلة أو الكالا الطويلة، والمطرّز يناسبه الكريستال. وللتفاصيل اقرئي <a href="{MAQALAT_PATH}ikhtiyar-maskat-al-arous/">كيف تختارين مسكة العروس حسب فستانك</a>.</p>
<p class="center"><a class="btn btn-primary" href="{MODELS_PATH}">عرض جميع الموديلات</a></p>"""

def _art_khotoba():
    return f"""
<p>مسكة الخطوبة تختلف عن مسكة العرس: الفستان غالبًا ملوّن، والجو أخفّ، فتحتمل المسكة الألوان واللمسات المرحة. هذه أفكار لمسكات خطوبة 2026 من شغلنا، وكلها ورد صناعي عالي الجودة لا يذبل.</p>
<h2>1. ألوان ناعمة: خوخي وزهري</h2>
<p>جربيرا وجوري بدرجات الخوخي والزهري الفاتح مع الجبسوفيل، تناسب فساتين البيج والزهري والأوف وايت.</p>
<ul class="pgrid">{model_cards(_cat(["zahri-naem", "naem-lulu"]))}</ul>
<h2>2. أبيض مع لمسة لون</h2>
<p>كالا أو توليب أبيض مع جوري أزرق أو زهري في الوسط: أنيقة وتظهر جميلة في الصور، وتناسب فستان الخطوبة بلون مطابق.</p>
<ul class="pgrid">{model_cards(_cat(["kala-jouri-azraq", "kala-zahr-wardi"]))}</ul>
<h2>3. الأبيض الكلاسيكي</h2>
<p>كثير من العرائس يفضّلن الأبيض حتى في الخطوبة، خصوصًا إذا كانت الخطوبة وكتب الكتاب في يوم واحد.</p>
<ul class="pgrid">{model_cards(_cat(["toulib-crystal", "jouri-abyad"]))}</ul>
<h2>كيف تختارين لون مسكة الخطوبة؟</h2>
<ul>
<li><b>فستان سادة:</b> مسكة بلون من نفس درجة الفستان أو أفتح بقليل.</li>
<li><b>فستان مطرّز أو لامع:</b> مسكة بيضاء أو بلون هادئ حتى لا تتزاحم التفاصيل.</li>
<li><b>أرسلي لنا صورة الفستان</b> على إنستغرام، ونقترح لك الألوان المناسبة.</li>
</ul>
<p>سعر مسكة الخطوبة عندنا مثل كل المسكات: {P['masaka']} دينارًا، و{withdel('masaka')} دينارًا شاملة التوصيل لأي محافظة.</p>
<p class="center"><a class="btn btn-primary" href="/masakat-arayes/khotoba/">مسكات الخطوبة</a></p>"""

def _art_tulip():
    return f"""
<p>مسكة العروس التوليب من أكثر المسكات طلبًا في الأردن: ناعمة وأنيقة، وتليق بالخطوبة وكتب الكتاب والعرس. هذه أشكالها عندنا وسعرها.</p>
<h2>أشكال مسكة التوليب</h2>
<h3>توليب باللولو والجبسوفيل</h3>
<p>إطار من اللولو والجبسوفيل حول التوليب، مع كشكش من التل. فخامة هادئة.</p>
<h3>توليب بالكريستال</h3>
<p>حبّات كريستال حول التوليب ومسكة ستراس فضية، لعروس تحب اللمعة.</p>
<h3>قوس التوليب</h3>
<p>توليب ينسدل على شكل قوس مع خيوط اللولو، تصميم مختلف يناسب الفستان الضيق.</p>
<ul class="pgrid">{model_cards([m for m in CATALOG if m["style"] in ("tulip", "crystal")])}</ul>
<h2>كم سعر مسكة العروس التوليب؟</h2>
<p>عند هدايا سلمى سعر مسكة التوليب {P['masaka']} دينارًا لكل الأشكال، و{withdel('masaka')} دينارًا شاملة التوصيل إلى أي محافظة في الأردن. والتوليب صناعي عالي الجودة يشبه الطبيعي ولا يذبل.</p>
<h2>التوليب أبيض فقط؟</h2>
<p>الأبيض هو الأكثر طلبًا، ونجهّز التوليب بالوردي أو بأي لون يناسب فستانك.</p>
<p class="center"><a class="btn btn-primary" href="/masakat-arayes/tulip/">مسكات التوليب</a></p>"""

AMMAN_AREAS = "عبدون، دابوق، خلدا، تلاع العلي، الجبيهة، صويلح، الشميساني، جبل عمّان، الصويفية، أم أذينة، طبربور، ماركا، المقابلين، الياسمين، خريبة السوق، أبو نصير، شفا بدران، مرج الحمام، ناعور، سحاب"
def _art_amman():
    return f"""
<p>تبحثين عن مسكة عروس في عمّان؟ نجهّز مسكات العروس في ورشتنا، ونوصلها لكل مناطق عمّان خلال يومين، وتعاينينها قبل أن تدفعي.</p>
<h2>التوصيل داخل عمّان</h2>
<ul>
<li><b>المدة:</b> خلال يومين من تأكيد الطلب، ويُفضَّل الحجز قبل المناسبة بثلاثة أيام.</li>
<li><b>السعر:</b> {DELIVERY} دينار للتوصيل.</li>
<li><b>الدفع:</b> عند الاستلام، نقدًا أو كليك، بعد المعاينة.</li>
</ul>
<p>نوصل لكل أحياء عمّان، منها: {AMMAN_AREAS}، وغيرها. ونوصل كذلك لإربد والزرقاء والسلط ومادبا وجرش وعجلون وكل المحافظات.</p>
<h2>سعر مسكة العروس في عمّان</h2>
<p>{P['masaka']} دينارًا لكل الموديلات، و{withdel('masaka')} دينارًا شاملة التوصيل لأي منطقة في عمّان.</p>
<h2>الأكثر طلبًا في عمّان</h2>
<ul class="pgrid">{model_cards(_cat(["toulib-crystal", "toulib-lulu", "kala-classic-strass", "peony-lulu"]))}</ul>
<p class="center"><a class="btn btn-primary" href="{MODELS_PATH}">عرض جميع الموديلات</a></p>"""

ARTICLES = [
    {"slug": "ajmal-maskat-arous-2026", "date": "2026-11-14", "title": "أجمل مسكات عروس 2026 في الأردن: أفكار بصور حقيقية",
     "desc": f"أجمل مسكات العروس لموسم 2026: توليب باللولو والكريستال، كالا طويلة، بيوني، مسكة القوس، ولمسات لون للخطوبة. صور حقيقية وسعر {P['masaka']} دينار.",
     "img": "sowar/maska-02.webp", "body": _art_best2026,
     "faq": [("ما أكثر مسكات العروس طلبًا في 2026؟", "التوليب الأبيض باللولو أو بالكريستال، ثم الكالا الطويلة بمقبض ستراس، والبيوني الممتلئ."),
             ("هل أجد هذه المسكات في الأردن؟", f"نعم، عند هدايا سلمى بسعر {P['masaka']} دينارًا لكل الموديلات، مع توصيل لكل المحافظات خلال يومين.")]},
    {"slug": "maskat-khotoba-2026", "date": "2026-11-14", "title": "مسكات خطوبة 2026: ألوان وأفكار تناسب فستان الخطوبة",
     "desc": f"أفكار مسكات خطوبة 2026 بألوان ناعمة: خوخي وزهري وأزرق، أو أبيض مع لمسة لون. كيف تختارين لون المسكة حسب الفستان، وسعرها {P['masaka']} دينار.",
     "img": "sowar/maska-24.webp", "body": _art_khotoba,
     "faq": [("ما لون مسكة الخطوبة المناسب؟", "لون من نفس درجة الفستان أو أفتح بقليل للفستان السادة، وأبيض أو لون هادئ للفستان المطرّز."),
             ("كم سعر مسكة الخطوبة؟", f"{P['masaka']} دينارًا، و{withdel('masaka')} دينارًا شاملة التوصيل لأي محافظة.")]},
    {"slug": "maskat-arous-tulip", "date": "2026-11-14", "title": "مسكة عروس توليب: أشكالها وسعرها في الأردن",
     "desc": f"مسكة العروس التوليب: باللولو والجبسوفيل، بالكريستال، أو على شكل قوس. صور حقيقية، وسعرها {P['masaka']} دينار مع توصيل لكل الأردن.",
     "img": "sowar/maska-08.webp", "body": _art_tulip,
     "faq": [("كم سعر مسكة العروس التوليب في الأردن؟", f"عند هدايا سلمى {P['masaka']} دينارًا لكل الأشكال، و{withdel('masaka')} مع التوصيل."),
             ("هل التوليب طبيعي؟", "لا، توليب صناعي عالي الجودة يشبه الطبيعي ولا يذبل.")]},
    {"slug": "maskat-arous-amman", "date": "2026-11-14", "title": "مسكة عروس في عمّان: توصيل خلال يومين لكل المناطق",
     "desc": f"مسكات عروس في عمّان بسعر {P['masaka']} دينار، توصيل خلال يومين لكل أحياء عمّان بـ{DELIVERY} دينار، ومعاينة ودفع عند الاستلام.",
     "img": "sowar/maska-17.webp", "body": _art_amman,
     "faq": [("هل توصلون مسكة العروس داخل عمّان؟", f"نعم، لكل مناطق عمّان خلال يومين، بسعر توصيل {DELIVERY} دينار."),
             ("كم سعر مسكة العروس في عمّان؟", f"{P['masaka']} دينارًا، و{withdel('masaka')} شاملة التوصيل.")]},
    {"slug": "ikhtiyar-maskat-al-arous", "title": "كيف تختارين مسكة العروس حسب فستانك؟",
     "desc": "دليل اختيار مسكة العروس حسب قَصّة الفستان وتفاصيله ولونه وطولك: منفوش، حورية، ساتان، دانتيل، كريستال، وفساتين الخطوبة الملوّنة، مع موديلات حقيقية.",
     "img": "model-turkish-qaws.webp", "body": _art_dress,
     "faq": [("ما أنسب مسكة لفستان منفوش؟", "مسكة دائرية ممتلئة مثل الجوري الأبيض الكلاسيك أو توليب اللولو، لأنها توازن حجم الفستان."),
             ("ما أنسب مسكة لفستان ضيق (حورية)؟", "مسكة منسدلة طويلة مثل المسكة التركية (القوس) أو قوس التوليب، لأنها تكمّل خط الفستان.")]},
    {"slug": "maskat-tulip-aw-kala", "title": "مسكة توليب ولا كالا؟ الفرق وأيهما يناسبك",
     "desc": "مقارنة بين مسكة العروس التوليب والكالا: الشكل، والإحساس، والفستان المناسب لكل واحدة، مع موديلات حقيقية من الاثنين بسعر 18 دينار.",
     "img": "model-kala-toulib-crystal.webp", "body": _art_tulip_calla,
     "faq": [("أيهما أجمل: مسكة التوليب أو الكالا؟", "الاثنتان جميلتان. التوليب أنعم وأنسب للفستان المنفوش والدانتيل، والكالا أكثر أناقة وأنسب للفستان الضيق والساتان."),
             ("هل يوجد مسكة تجمع التوليب والكالا؟", "نعم، مثل موديل كالا وتوليب بالكريستال، وموديل جوري زهري وتوليب.")]},
    {"slug": "sier-maskat-al-arous-fi-al-urdun", "title": "كم سعر مسكة العروس في الأردن؟",
     "desc": f"ما الذي يحدد سعر مسكة العروس في الأردن: ورد طبيعي أو صناعي، الحجم، الإكسسوارات والتوصيل. وسعر المسكة عند هدايا سلمى {P['masaka']} دينار لكل الموديلات.",
     "img": "model-toulib-lulu.webp", "body": _art_price,
     "faq": [FAQ[1], FAQ[18], ("هل مسكة الورد الصناعي أفضل من الطبيعي؟", "الصناعي عالي الجودة لا يذبل ويبقى ذكرى بعد المناسبة، ويُجهَّز مسبقًا دون قلق يوم العرس. الطبيعي له رائحة، لكنه يذبل خلال أيام.")]},
]
def art_path(a): return MAQALAT_PATH + a["slug"] + "/"

def build_article(a):
    trail = [("نصائح للعروس", MAQALAT_PATH), (a["title"], art_path(a))]
    bc, bsch = breadcrumb(trail)
    others = "".join(f'<li><a href="{art_path(x)}">{E(x["title"])}</a></li>' for x in ARTICLES if x is not a)
    body = bc + f"""
<article class="section article"><div class="container narrow">
  <h1>{E(a["title"])}</h1>
  <p class="article-meta">هدايا سلمى · متجر أردني مختص بمسكات العرايس</p>
  {a["body"]()}
  <div class="actions">{cta("اسألينا برسالة على إنستغرام", "btn btn-primary", "cta_article")}</div>
  <h2>أسئلة سريعة</h2>
  {faq_html(a["faq"])}
  <nav class="related"><p>مقالات أخرى</p><ul>{others}</ul></nav>
</div></article>"""
    art = {"@type": "Article", "headline": a["title"], "description": a["desc"], "inLanguage": "ar",
           "image": SITE + "/assets/img/" + a["img"], "datePublished": a.get("date", "2026-10-25"), "dateModified": TODAY,
           "author": {"@id": STORE_ID}, "publisher": {"@id": STORE_ID}, "mainEntityOfPage": SITE + art_path(a)}
    write(art_path(a), layout("style-article", art_path(a), f"{a['title']} | هدايا سلمى", a["desc"], body,
          [bsch, art, faq_schema(a["faq"])], og_img=a["img"]))

def build_articles_index():
    bc, bsch = breadcrumb([("نصائح للعروس", MAQALAT_PATH)])
    cards = "".join('<li><a href="' + art_path(a) + '">' + img(a["img"], a["title"], w=900, h=1141)
                    + '<span class="label"><b>' + E(a["title"]) + '</b></span></a></li>' for a in ARTICLES)
    body = bc + f"""
<section class="section"><div class="container">
  <h1>نصائح للعروس</h1>
  <p class="section-intro">مقالات قصيرة تساعدك تختاري مسكتك: حسب الفستان، والنوع، والسعر.</p>
  <ul class="rail rail-grid">{cards}</ul>
</div></section>"""
    write(MAQALAT_PATH, layout("style-articles", MAQALAT_PATH, "نصائح للعروس: اختيار مسكة العروس | هدايا سلمى",
          "مقالات تساعد العروس تختار مسكتها: حسب الفستان، توليب أو كالا، وكم سعر مسكة العروس في الأردن.", body, [bsch]))

def articles_block():
    lis = "".join(f'<li><a href="{art_path(a)}">{E(a["title"])}</a></li>' for a in ARTICLES)
    return f"""<section class="section"><div class="container narrow">
  <div class="section-head"><h2>نصائح للعروس</h2><a href="{MAQALAT_PATH}">كل المقالات {ARROW}</a></div>
  <ul class="art-list">{lis}</ul>
</div></section>"""

def all_paths():
    return [PAGES[k]["path"] for k in ["home"] + NAV_ORDER] + [s["path"] for s in STYLES] + [MODELS_PATH, SOWAR_PATH] + [model_path(m) for m in MODELS] + [MAQALAT_PATH] + [art_path(a) for a in ARTICLES]

def build_sitemap():
    imgs = {model_path(m): [m["img"]] for m in MODELS}
    imgs[SOWAR_PATH] = [c["img"] for c in CATALOG]
    imgs[MODELS_PATH] = [c["img"] for c in CATALOG]
    for st in STYLES: imgs[st["path"]] = [ph[0] for ph in st["photos"]]
    def entry(p):
        im = "".join(f"<image:image><image:loc>{SITE}/assets/img/{x}</image:loc></image:image>" for x in imgs.get(p, []))
        return f"  <url><loc>{SITE}{p}</loc><lastmod>{TODAY}</lastmod>{im}</url>\n"
    urls = "".join(entry(p) for p in all_paths())
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n{urls}</urlset>\n')

def build_llms():
    lines = [
        "# Salma Gifts - هدايا سلمى",
        "",
        f"> متجر أردني أونلاين لهدايا المناسبات حسب الطلب: مسكات عروس 2026 / مسكات العرايس / مسكة العروس (توليب، كريستال، كالا، جوري، بيوني — ورد صناعي لا يذبل)، صواني الخطوبة والدبل من المرآة بالأسماء، بكجات كتب الكتاب، صندوق المهر وهدايا التخرج. توصيل لكل محافظات الأردن، ومعاينة ودفع عند الاستلام. الطلب عبر رسائل إنستغرام @salma.gifts1. شعارنا: {SLOGAN}",
        "",
        "Salma Gifts is an online gift shop in Jordan making personalized engagement and wedding items: artificial-flower bridal bouquets (tulip, crystal, calla, rose/jouri, peony; any color to match the dress), mirror engagement ring trays with the couple's names (wooden back against breaking), marriage-contract (katb el-kitab) signature book packages, dowry (mahr) boxes and graduation gifts. 1500+ orders completed, 120+ orders a week. Delivery to all governorates of Jordan for 2 JOD within two days. Cash on delivery with inspection before paying. Orders via Instagram DM @salma.gifts1.",
        "",
        "## الأسعار (دينار أردني، بدون التوصيل)",
        f"- مسكة العروس، كل الأنواع: {P['masaka']} بدل {P['masaka_old']} (عرض خاص) — {withdel('masaka')} مع التوصيل (ورد صناعي عالي الجودة، 20–25 وردة).",
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
        "",
        f"## صور مسكات عروس 2026 ({SITE}{SOWAR_PATH})",
    ] + [f"- {name}" for n, name in SOWAR] + [
        "",
        f"## موديلات المسكات ({SITE}{MODELS_PATH})",
    ] + [f"- [{m['h1']}]({SITE}{model_path(m)}): {m['lead']}" for m in CATALOG] + [
        "",
        f"## نصائح للعروس ({SITE}{MAQALAT_PATH})",
    ] + [f"- [{a['title']}]({SITE}{art_path(a)}): {a['desc']}" for a in ARTICLES] + [
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

# =====================================================================
# صور مسكات عروس 2026 (معرض الصور)
# =====================================================================
SOWAR_PATH = "/masakat-arayes/sowar/"
SOWAR = [
 ("01","مسكة عروس جوري أبيض مع جبسوفيل وفيونكة دانتيل"),
 ("02","مسكة عروس توليب أبيض بإطار كريستال"),
 ("03","مسكة عروس توليب أبيض بالكريستال ومقبض ستراس"),
 ("04","مسكة عروس كالا وجوري أزرق"),
 ("05","مسكة عروس كالا أبيض"),
 ("06","مسكة عروس توليب بالكريستال"),
 ("07","مسكة عروس بيوني أبيض باللولو"),
 ("08","مسكة عروس توليب أبيض باللولو والجبسوفيل"),
 ("09","مسكة عروس توليب مع بوتونيير للعريس"),
 ("10","مسكة عروس كالا باللولو بمقبض كريستال"),
 ("11","مسكة عروس كالا أبيض بمقبض ستراس"),
 ("12","مسكة عروس كالا وتوليب بالكريستال"),
 ("13","مسكة عروس كالا أبيض بمقبض دانتيل"),
 ("14","مسكة عروس كالا أبيض مع أغصان ناعمة"),
 ("15","مسكة عروس كالا وجوري أبيض"),
 ("16","مسكة عروس جوري أبيض بفيونكة دانتيل"),
 ("17","مسكة عروس توليب باللولو والكريستال"),
 ("18","مسكة عروس كالا وجوري زهري"),
 ("19","مسكة عروس توليب أبيض ناعمة باللولو"),
 ("20","مسكة عروس جربيرا وجوري بألوان ناعمة"),
 ("21","مسكة عروس قوس التوليب باللولو"),
 ("22","مسكة عروس توليب أبيض بمقبض لولو"),
 ("23","مسكة عروس جوري أحمر بمقبض لولو"),
 ("24","مسكة عروس بألوان ناعمة باللولو"),
 ("25","مسكة عروس بيوني أبيض بمقبض دانتيل"),
]

def build_sowar():
    trail = [(PAGES["masakat"]["nav"], PAGES["masakat"]["path"]), ("صور مسكات عروس 2026", SOWAR_PATH)]
    head, bsch = page_intro(trail, "صور مسكات عروس 2026",
        f"{len(SOWAR)} صورة لمسكات عروس من تصاميمنا: توليب أبيض، كالا، جوري، بيوني وكريستال، بلولو ودانتيل. كلها ورد صناعي عالي الجودة لا يذبل، بسعر {P['masaka']} دينار حاليًا، و{withdel('masaka')} مع التوصيل لكل محافظات الأردن.", "masaka")
    cards = model_cards(CATALOG, eager=2)
    body = head + f"""
<section class="section"><div class="container">
  <h2>اختاري المسكة اللي بتشبهك</h2>
  <p class="section-intro">اضغطي على المسكة لتشوفي صورتها كبيرة وتفاصيلها، ونجهّزها بلون يناسب فستانك.</p>
  <ul class="pgrid">{cards}</ul>
  <p class="center"><a class="btn btn-primary" href="{MODELS_PATH}">عرض جميع الموديلات</a></p>
</div></section>
{section("قبل الحجز", promise_list(), cls="tint")}
<section class="section"><div class="container narrow">
  <h2>أسئلة عن مسكات العروس</h2>
  {faq_html([FAQ[1], FAQ[13], FAQ[14], FAQ[7]])}
  {related("masakat")}
</div></section>"""
    gallery = {"@type": "ImageGallery", "name": "صور مسكات عروس 2026 — هدايا سلمى", "url": SITE + SOWAR_PATH,
               "image": [{"@type": "ImageObject", "contentUrl": SITE + "/assets/img/sowar/maska-" + n + ".webp", "name": name} for n, name in SOWAR]}
    write(SOWAR_PATH, layout("style-sowar", SOWAR_PATH,
        f"صور مسكات عروس 2026: {len(SOWAR)} صورة مسكة عروس بـ{P['masaka']} دينار | هدايا سلمى",
        f"صور مسكات عروس 2026 من هدايا سلمى: توليب أبيض، كالا، جوري، بيوني وكريستال باللولو والدانتيل. ورد صناعي لا يذبل بـ{P['masaka']} دينار و{withdel('masaka')} مع التوصيل لكل الأردن.",
        body, [bsch, gallery, faq_schema([FAQ[1], FAQ[13], FAQ[14], FAQ[7]])], og_img="sowar/maska-02.webp"))

if __name__ == "__main__":
    build_home(); build_masakat()
    for s in STYLES:
        build_style(s)
    build_models_index(); build_sowar()
    for m in MODELS:
        build_model(m)
    build_articles_index()
    for a in ARTICLES:
        build_article(a)
    build_sawani(); build_bakjat(); build_mahr(); build_grad()
    build_tawseel(); build_faq(); build_404(); build_sitemap(); build_llms()
    print("تم بناء الموقع.")
