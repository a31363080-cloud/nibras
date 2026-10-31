---
title: Nibras
emoji: 🛠️
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
---

# نبراس

موقع أدوات ذكاء اصطناعي بالعربية: نص إلى صوت (في المتصفح)، توليد صور، تلخيص فيديو.

## النشر على Hugging Face Spaces
1. أنشئ Space جديداً من نوع **Docker** وارفع هذه الملفات.
2. من Settings ← Variables and secrets أضف Secret باسم `HF_TOKEN` (توكن بصلاحية Inference).
3. أضف Variables: `SITE_URL` (عنوان موقعك النهائي بلا شرطة في آخره)، و`CONTACT_EMAIL` (بريدك الظاهر في صفحة التواصل).
4. بعد قبول AdSense: أضف `ADSENSE_CLIENT` (مثل ca-pub-...) و`ADSENSE_SLOT`. تظهر الإعلانات وملف ads.txt تلقائياً.
5. اختيارياً: `IMAGE_MODEL` و`LLM_MODEL` لتغيير النماذج.

## الصفحات
`/` الرئيسية، `/tools/<أداة>` لكل أداة (6 أدوات)، `/about` و`/privacy` و`/contact` (مطلوبة لـ AdSense)، `/sitemap.xml` و`/robots.txt`. أرسل sitemap.xml إلى Google Search Console بعد ربط الدومين.

## التشغيل محلياً
```
pip install -r requirements.txt
HF_TOKEN=hf_xxx uvicorn app:app --port 7860
```

## ملاحظات
- حد الاستخدام: 6 صور و10 تلخيصات في الساعة لكل زائر (غيّره في `LIMITS`).
- يوتيوب يحجب كثيراً من عناوين الخوادم السحابية، لذلك قد يفشل جلب نص الفيديو. الواجهة تتيح لصق النص يدوياً كبديل.
- حصة Inference المجانية محدودة. عند كثرة الزوار ستحتاج حساباً مدفوعاً أو نموذجاً مستضافاً بنفسك.
