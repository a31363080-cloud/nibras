"""قوالب الصفحات: كل أداة لها صفحة مستقلة بعنوان ووصف وأسئلة شائعة لمحركات البحث."""
import html
import json
import os

SITE = "نبراس"
ADSENSE_CLIENT = os.getenv("ADSENSE_CLIENT", "")      # مثل ca-pub-1234567890123456
ADSENSE_SLOT = os.getenv("ADSENSE_SLOT", "")          # رقم وحدة الإعلان
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "contact@your-domain.com")

# ------------------------------------------------------------------ بيانات الأدوات
TOOLS = [
    dict(
        slug="text-to-speech", panel="tts", name="نص إلى صوت",
        title="تحويل النص إلى صوت عربي مجاناً",
        desc="حوّل أي نص عربي إلى صوت مسموع مجاناً وبلا تسجيل. اختر الصوت والسرعة ودرجة الصوت واستمع فوراً من المتصفح.",
        blurb="استمع إلى أي نص عربي بصوت واضح، مع التحكم في السرعة.",
        intro="اكتب نصاً عربياً أو الصقه، ثم اختر صوتاً واضغط تشغيل. تتوفر أصوات عربية بلهجات جزائرية وسعودية ومصرية، حتى 3000 حرف في المرة.",
        steps=["اكتب النص أو الصقه في الخانة.", "اختر الصوت من القائمة وعدّل السرعة.", "اضغط تشغيل للاستماع، أو إيقاف مؤقت لاستكمال الاستماع لاحقاً."],
        faqs=[
            ("هل الأداة مجانية؟", "نعم، مجانية بالكامل وبلا تسجيل ولا حد للاستخدام."),
            ("ما الفرق بين أصوات الموقع وأصوات الجهاز؟", "أصوات الموقع عربية جاهزة تعمل على كل الأجهزة. أصوات الجهاز تأتي من نظامك وتعمل بلا اتصال، لكنها قد لا تتضمن العربية حتى تثبّت حزمتها من إعدادات اللغة."),
            ("هل يُحفظ نصي؟", "لا نحفظ النصوص. عند اختيار أحد أصوات الموقع يُرسل النص إلى خادمنا ثم إلى خدمة تحويل الصوت لتوليد الملف، ولا يغادر النص جهازك عند اختيار صوت الجهاز."),
        ],
    ),
    dict(
        slug="image-generator", panel="image", name="توليد صور",
        title="توليد صور بالذكاء الاصطناعي من وصف عربي",
        desc="اكتب وصف الصورة بالعربية واحصل على صورة مولّدة بالذكاء الاصطناعي بنمط واقعي أو كرتوني أو رسم زيتي. مجاناً.",
        blurb="صف الصورة بالعربية واحصل عليها بالنمط والمقاس الذي تريد.",
        intro="اكتب ما تريد رؤيته بالعربية. تُترجم الفكرة تلقائياً إلى وصف يفهمه نموذج الصور، ثم تظهر لك الصورة جاهزة للتحميل.",
        steps=["صف المشهد بالتفصيل: المكان والإضاءة والألوان.", "اختر النمط والمقاس.", "اضغط توليد وانتظر نحو نصف دقيقة، ثم حمّل الصورة."],
        faqs=[
            ("كم تستغرق الصورة؟", "من 10 ثوانٍ إلى دقيقة، حسب ازدحام الخادم."),
            ("كيف أحصل على نتيجة أفضل؟", "اذكر الموضوع ثم المكان ثم الإضاءة والألوان. الوصف المحدد يعطي صورة أدق من الوصف العام."),
            ("هل يمكن استخدام الصور تجارياً؟", "راجع ترخيص النموذج المستخدم قبل الاستخدام التجاري. نحن لا نضمن ذلك."),
            ("لماذا لا تظهر الكتابة العربية داخل الصورة بشكل صحيح؟", "نماذج الصور ضعيفة في رسم الحروف العربية. اطلب الصورة بلا نص وأضف الكتابة لاحقاً ببرنامج تصميم."),
        ],
    ),
    dict(
        slug="video-summarizer", panel="video", name="تلخيص فيديو",
        title="تلخيص فيديو يوتيوب بالذكاء الاصطناعي",
        desc="الصق رابط فيديو يوتيوب واحصل على ملخص بنقاط بالعربية في ثوانٍ. وفّر وقت المشاهدة وانظر ما يستحق.",
        blurb="لخّص فيديو طويلاً في بضع نقاط قبل أن تقرر مشاهدته.",
        intro="الصق رابط فيديو يوتيوب، أو الصق نصه إن لم يعمل الرابط. نقرأ النص ونعطيك الملخص باللغة التي تختارها.",
        steps=["الصق رابط الفيديو في الخانة.", "اختر طول الملخص ولغته.", "اضغط لخّص. إن فشل الرابط فافتح قسم لصق النص وضع نص الفيديو هناك."],
        faqs=[
            ("هل تعمل الأداة مع كل الفيديوهات؟", "تعمل مع الفيديوهات التي لها ترجمة أو نص مكتوب. الفيديوهات بلا ترجمة تحتاج لصق النص يدوياً."),
            ("ما أطول فيديو يمكن تلخيصه؟", "نقرأ نحو 30 إلى 40 دقيقة من الكلام. ما زاد عن ذلك يُقتطع."),
            ("هل الملخص دقيق؟", "هو مبني على نص الفيديو فقط، لكنه قد يخطئ أحياناً. راجع الأجزاء المهمة في الفيديو نفسه."),
        ],
    ),
    dict(
        slug="arabic-tashkeel", panel="text", mode="tashkeel", name="تشكيل النص",
        title="تشكيل النص العربي آلياً بالذكاء الاصطناعي",
        desc="أضف التشكيل (الفتحة والضمة والكسرة) إلى أي نص عربي تلقائياً بالذكاء الاصطناعي، ثم انسخه. مجاناً وبلا تسجيل.",
        blurb="أضف الحركات إلى النص العربي بضغطة واحدة.",
        intro="الصق نصاً عربياً غير مشكول واحصل عليه مشكولاً. مناسب للنصوص القصيرة والوسط، حتى 2000 حرف في المرة.",
        steps=["الصق النص العربي في الخانة.", "اضغط تشكيل.", "انسخ النتيجة وراجعها."],
        faqs=[
            ("هل التشكيل مضمون الصحة؟", "لا. يخطئ الذكاء الاصطناعي أحياناً في المواضع المعقدة. راجع النصوص الدينية والرسمية قبل نشرها."),
            ("هل يغيّر الأداة كلمات النص؟", "لا نطلب منه ذلك، يضيف الحركات فقط. قارن النتيجة بالأصل عند الحاجة."),
        ],
        limit=2000,
    ),
    dict(
        slug="arabic-proofreader", panel="text", mode="proofread", name="تدقيق إملائي",
        title="تدقيق إملائي ونحوي للنص العربي",
        desc="صحّح الأخطاء الإملائية والنحوية وعلامات الترقيم في نصك العربي بالذكاء الاصطناعي، وانسخ النص المصحّح.",
        blurb="صحّح الأخطاء الإملائية وعلامات الترقيم في نصك.",
        intro="الصق نصك العربي ونصحّح الإملاء والنحو والترقيم مع الإبقاء على أسلوبك ومعناك. حتى 3000 حرف في المرة.",
        steps=["الصق النص في الخانة.", "اضغط دقّق.", "قارن النتيجة بنصك وانسخ ما يناسبك."],
        faqs=[
            ("هل يغيّر الأداة أسلوبي في الكتابة؟", "نطلب منها تصحيح الأخطاء فقط والإبقاء على الكلمات والمعنى."),
            ("هل تصلح للأبحاث الأكاديمية؟", "تساعد في الإملاء والترقيم، لكن المراجعة اللغوية النهائية تبقى عليك."),
        ],
        limit=3000,
    ),
    dict(
        slug="text-summarizer", panel="text", mode="summarize", name="تلخيص نص",
        title="تلخيص النصوص العربية الطويلة بالذكاء الاصطناعي",
        desc="الصق مقالاً أو نصاً طويلاً بالعربية واحصل على ملخص بنقاط في ثوانٍ، بالطول واللغة التي تختارها.",
        blurb="اختصر المقالات والنصوص الطويلة في نقاط واضحة.",
        intro="الصق مقالاً أو تقريراً أو رسالة طويلة، واختر طول الملخص. حتى 12000 حرف في المرة.",
        steps=["الصق النص الطويل.", "اختر طول الملخص ولغته.", "اضغط لخّص وانسخ النتيجة."],
        faqs=[
            ("هل يخترع الملخص معلومات؟", "نطلب منه الاعتماد على النص فقط، لكن تبقى المراجعة مطلوبة."),
            ("بأي لغات يمكن التلخيص؟", "النص بالعربية أو الإنجليزية أو الفرنسية، والملخص بإحداها."),
        ],
        limit=12000,
    ),
]
BY_SLUG = {t["slug"]: t for t in TOOLS}


# ------------------------------------------------------------------ مكونات
def esc(s):
    return html.escape(s, quote=True)


def ad(wide=False):
    if not (ADSENSE_CLIENT and ADSENSE_SLOT):
        return ""
    cls = "ad wide" if wide else "ad"
    return (f'<div class="{cls}"><ins class="adsbygoogle" style="display:block" data-ad-client="{esc(ADSENSE_CLIENT)}" '
            f'data-ad-slot="{esc(ADSENSE_SLOT)}" data-ad-format="auto" data-full-width-responsive="true"></ins>'
            '<script>(adsbygoogle=window.adsbygoogle||[]).push({});</script></div>')


def panel(t):
    p = t["panel"]
    if p == "tts":
        return '''<section class="panel" id="tts">
<label for="txt">النص</label>
<textarea id="txt" maxlength="3000">السلام عليكم ورحمة الله. هذه تجربة لأداة تحويل النص إلى صوت باللغة العربية. يمكنك تغيير السرعة ودرجة الصوت، ثم الضغط على زر التشغيل.</textarea>
<div class="row">
<div><label for="voice">الصوت</label><select id="voice"></select></div>
<div><label for="rate">السرعة: <span id="rv">1.0</span></label><input type="range" id="rate" min="0.5" max="1.6" step="0.1" value="1"></div>
<div><label for="pitch">درجة الصوت: <span id="pv">1.0</span></label><input type="range" id="pitch" min="0.5" max="1.5" step="0.1" value="1"></div>
</div>
<div class="actions"><button class="btn primary" id="play">تشغيل</button><button class="btn" id="pause">إيقاف مؤقت</button><button class="btn" id="stop">إيقاف</button>
<span class="meta"><span id="cnt">0</span> / 3000 حرف</span><span class="meta" id="tts-st"></span></div>
<div class="note" id="ttsNote" hidden></div></section>'''
    if p == "image":
        return '''<section class="panel" id="image">
<label for="ip">وصف الصورة</label>
<textarea id="ip" maxlength="500" style="min-height:110px">قصر أندلسي عند الغروب، ألوان دافئة، تفاصيل دقيقة</textarea>
<div class="row"><div><label>النمط</label><div class="chips" id="styles">
<button aria-pressed="true">واقعي</button><button aria-pressed="false">رسم زيتي</button><button aria-pressed="false">كرتوني</button><button aria-pressed="false">ثلاثي الأبعاد</button></div></div>
<div><label for="size">المقاس</label><select id="size"><option>مربع 1:1</option><option>أفقي 16:9</option><option>عمودي 9:16</option></select></div></div>
<div class="actions"><button class="btn primary" id="igo">ولّد الصورة</button><span class="meta" id="ist"></span></div>
<div class="note err" id="ierr" hidden></div>
<div class="result" id="ires" hidden><img id="iimg" alt="الصورة المولّدة"><div class="actions"><a class="btn" id="idl" download="image.jpg">تحميل الصورة</a></div></div></section>'''
    if p == "video":
        return '''<section class="panel" id="video">
<label for="vu">رابط الفيديو</label>
<input type="text" id="vu" dir="ltr" placeholder="https://www.youtube.com/watch?v=...">
<div class="row"><div><label for="vl">طول الملخص</label><select id="vl"><option>قصير (5 نقاط)</option><option>متوسط (10 نقاط)</option><option>مفصّل</option></select></div>
<div><label for="vo">لغة الملخص</label><select id="vo"><option>العربية</option><option>English</option><option>Français</option></select></div></div>
<details><summary>الرابط لا يعمل؟ الصق نص الفيديو بدلاً منه</summary>
<label for="vt" style="margin-top:8px">نص الفيديو</label><textarea id="vt" style="min-height:120px"></textarea></details>
<div class="actions"><button class="btn primary" id="vgo">لخّص</button><span class="meta" id="vst"></span></div>
<div class="note err" id="verr" hidden></div>
<div class="result" id="vres" hidden><pre id="vsum"></pre><div class="actions"><button class="btn" id="vcopy">نسخ الملخص</button></div></div></section>'''
    # text tools
    verb = {"tashkeel": "شكّل", "proofread": "دقّق", "summarize": "لخّص"}[t["mode"]]
    extra = ""
    if t["mode"] == "summarize":
        extra = ('<div class="row"><div><label for="tl">طول الملخص</label><select id="tl"><option>قصير (5 نقاط)</option><option>متوسط (10 نقاط)</option><option>مفصّل</option></select></div>'
                 '<div><label for="to">لغة الملخص</label><select id="to"><option>العربية</option><option>English</option><option>Français</option></select></div></div>')
    return f'''<section class="panel" id="text" data-mode="{t['mode']}">
<label for="tx">النص</label>
<textarea id="tx" maxlength="{t['limit']}" placeholder="الصق النص هنا"></textarea>
{extra}
<div class="actions"><button class="btn primary" id="tgo">{verb}</button><span class="meta"><span id="tcnt">0</span> / {t['limit']} حرف</span><span class="meta" id="tst"></span></div>
<div class="note err" id="terr" hidden></div>
<div class="result" id="tres" hidden><pre id="tout" dir="auto"></pre><div class="actions"><button class="btn" id="tcopy">نسخ النتيجة</button></div></div></section>'''


def layout(title, desc, path, body, base, jsonld=None, robots="index,follow"):
    full_title = f"{title} | {SITE}" if title != SITE else f"{SITE} | أدوات ذكاء اصطناعي بالعربية"
    nav = "".join(f'<a href="/tools/{t["slug"]}">{esc(t["name"])}</a>' for t in TOOLS)
    def _ld(j):
        data = json.dumps(j, ensure_ascii=False).replace("</", "<\\/")
        return '<script type="application/ld+json">' + data + '</script>'
    ld = "".join(_ld(j) for j in (jsonld or []))
    adsense = (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={esc(ADSENSE_CLIENT)}" crossorigin="anonymous"></script>'
               if ADSENSE_CLIENT else "")
    return f'''<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{esc(base + path)}">
<meta property="og:type" content="website"><meta property="og:locale" content="ar_AR">
<meta property="og:title" content="{esc(full_title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{esc(base + path)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Reem+Kufi:wght@500;700&family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/static/style.css">
{adsense}{ld}
</head><body>
<div class="wrap">
<header><a class="brand" href="/">نب<span>راس</span></a><nav class="top" aria-label="الأدوات">{nav}</nav></header>
{body}
<footer><div class="flinks"><a href="/about">من نحن</a><a href="/privacy">سياسة الخصوصية</a><a href="/contact">تواصل معنا</a></div>
<div>{SITE} · أدوات ذكاء اصطناعي بالعربية</div></footer>
</div>
<script src="/static/app.js" defer></script>
</body></html>'''


# ------------------------------------------------------------------ صفحات
def home(base):
    cards = "".join(
        f'<a class="card" href="/tools/{t["slug"]}"><b>{esc(t["name"])}</b><span>{esc(t["blurb"])}</span></a>' for t in TOOLS)
    body = f'''<section class="hero"><h1>أدوات ذكاء اصطناعي بالعربية</h1>
<p>حوّل النص إلى صوت، ولّد الصور من وصف عربي، لخّص الفيديوهات والمقالات، وشكّل النصوص ودقّقها. مجاناً وبلا تسجيل.</p></section>
<div class="cards">{cards}</div>{ad(True)}
<section class="how"><div><b>بالعربية أولاً</b><span>واجهة من اليمين إلى اليسار وأدوات تفهم العربية.</span></div>
<div><b>بلا تسجيل</b><span>افتح الأداة واستخدمها فوراً.</span></div>
<div><b>تعمل من الجوال</b><span>الصفحات خفيفة وتناسب الشاشات الصغيرة.</span></div></section>'''
    ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": SITE, "url": base + "/", "inLanguage": "ar"}]
    return layout(SITE, "أدوات ذكاء اصطناعي مجانية بالعربية: نص إلى صوت، توليد صور، تلخيص فيديو، تشكيل وتدقيق النصوص.", "/", body, base, ld)


def tool_page(t, base):
    steps = "".join(f"<li>{esc(s)}</li>" for s in t["steps"])
    faqs = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in t["faqs"])
    related = "".join(f'<a class="card" href="/tools/{o["slug"]}"><b>{esc(o["name"])}</b><span>{esc(o["blurb"])}</span></a>'
                      for o in TOOLS if o["slug"] != t["slug"])
    body = f'''<section class="hero"><h1>{esc(t["title"])}</h1><p>{esc(t["intro"])}</p></section>
<div class="grid"><div>{panel(t)}</div><aside>{ad()}</aside></div>
<section class="prose"><h2>طريقة الاستخدام</h2><ol>{steps}</ol>
<h2>أسئلة شائعة</h2><div class="faq">{faqs}</div></section>
{ad(True)}
<section><h2 class="h2">أدوات أخرى</h2><div class="cards">{related}</div></section>'''
    ld = [
        {"@context": "https://schema.org", "@type": "WebApplication", "name": t["name"], "url": f"{base}/tools/{t['slug']}",
         "description": t["desc"], "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "inLanguage": "ar",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faqs"]]},
    ]
    return layout(t["title"], t["desc"], f"/tools/{t['slug']}", body, base, ld)


def about(base):
    body = f'''<section class="prose page"><h1>من نحن</h1>
<p>{SITE} موقع يجمع أدوات ذكاء اصطناعي تعمل بالعربية: تحويل النص إلى صوت، توليد الصور، تلخيص الفيديو والنصوص، وتشكيل النص وتدقيقه.</p>
<p>هدفنا أن تكون هذه الأدوات سهلة ومجانية وتعمل من الجوال بلا تسجيل. تعتمد بعض الأدوات على نماذج ذكاء اصطناعي مستضافة لدى طرف ثالث، وقد تخطئ نتائجها، لذلك نوصي بمراجعة المخرجات قبل الاعتماد عليها.</p>
<p>لأي اقتراح أو ملاحظة، تجد طريقة التواصل في صفحة <a href="/contact">تواصل معنا</a>.</p></section>'''
    return layout("من نحن", f"تعرّف على {SITE}: أدوات ذكاء اصطناعي مجانية بالعربية.", "/about", body, base)


def privacy(base):
    body = f'''<section class="prose page"><h1>سياسة الخصوصية</h1>
<p>آخر تحديث: أكتوبر 2026.</p>
<h2>ما نجمعه</h2>
<p>لا نطلب تسجيلاً ولا نجمع أسماء أو عناوين بريد من مستخدمي الأدوات.</p>
<h2>النصوص والروابط التي تدخلها</h2>
<p>عند اختيار صوت الجهاز في أداة النص إلى صوت يبقى النص داخل متصفحك. أما أصوات الموقع وأدوات توليد الصور وتلخيص الفيديو والنصوص وتشكيلها وتدقيقها فتُرسل ما تدخله إلى خادمنا ثم إلى مزوّد خارجي (خدمة تحويل الصوت أو مزوّد نماذج الذكاء الاصطناعي) لمعالجته وإرجاع النتيجة. لا نحتفظ بهذه المدخلات في قاعدة بيانات. لا تُدخل معلومات شخصية أو سرية في هذه الأدوات.</p>
<p>قد نحتفظ مؤقتاً بعنوان IP في ذاكرة الخادم لتطبيق حد الاستخدام، ويُمحى عند إعادة تشغيل الخادم.</p>
<h2>الإعلانات وملفات تعريف الارتباط</h2>
<p>قد نعرض إعلانات عبر Google AdSense. تستخدم Google وشركاؤها ملفات تعريف الارتباط لعرض إعلانات مبنية على زياراتك السابقة لهذا الموقع ومواقع أخرى. يمكنك إدارة الإعلانات المخصصة أو إيقافها من <a href="https://adssettings.google.com" target="_blank" rel="noopener">إعدادات إعلانات Google</a>.</p>
<h2>روابط خارجية</h2>
<p>قد يحتوي الموقع على روابط لمواقع أخرى لا نتحكم في سياساتها.</p>
<h2>التواصل</h2>
<p>لأي سؤال عن الخصوصية، راسلنا عبر صفحة <a href="/contact">تواصل معنا</a>.</p></section>'''
    return layout("سياسة الخصوصية", f"كيف يتعامل {SITE} مع بياناتك والإعلانات وملفات تعريف الارتباط.", "/privacy", body, base)


def contact(base):
    body = f'''<section class="prose page"><h1>تواصل معنا</h1>
<p>للاقتراحات والملاحظات والإبلاغ عن مشكلة، راسلنا على البريد التالي:</p>
<p dir="ltr" class="mail">{esc(CONTACT_EMAIL)}</p></section>'''
    return layout("تواصل معنا", f"طرق التواصل مع {SITE}.", "/contact", body, base)


def sitemap(base):
    paths = ["/"] + [f"/tools/{t['slug']}" for t in TOOLS] + ["/about", "/privacy", "/contact"]
    urls = "".join(f"<url><loc>{esc(base + p)}</loc></url>" for p in paths)
    return f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
