"""نبراس: خادم توليد الصور وتلخيص الفيديو بالعربية.

المتغيرات البيئية (Secrets في HF Space):
  HF_TOKEN       مطلوب. توكن Hugging Face بصلاحية Inference.
  IMAGE_MODEL    اختياري. الافتراضي black-forest-labs/FLUX.1-schnell
  LLM_MODEL      اختياري. الافتراضي Qwen/Qwen2.5-72B-Instruct
  SITE_URL       اختياري لكن مهم: عنوان الموقع النهائي (https://example.com) لـ sitemap وcanonical
  ADSENSE_CLIENT / ADSENSE_SLOT   اختياري: لتفعيل الإعلانات
  CONTACT_EMAIL  بريد صفحة التواصل
"""
import base64
import io
import os
import re
import time
from collections import defaultdict, deque
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

import pages

HF_TOKEN = os.getenv("HF_TOKEN", "")
IMAGE_MODEL = os.getenv("IMAGE_MODEL", "black-forest-labs/FLUX.1-schnell")
LLM_MODEL = os.getenv("LLM_MODEL", "Qwen/Qwen2.5-72B-Instruct")

# حد بسيط للطلبات لكل عنوان IP: (عدد الطلبات، المدة بالثواني)
LIMITS = {"image": (6, 3600), "summarize": (10, 3600), "text": (30, 3600), "tts": (30, 3600)}
_hits: dict = defaultdict(deque)

app = FastAPI(title="نبراس")


def _client():
    if not HF_TOKEN:
        raise HTTPException(503, "الخادم غير مهيأ: ضع HF_TOKEN في إعدادات Space.")
    from huggingface_hub import InferenceClient
    return InferenceClient(token=HF_TOKEN, timeout=120)


def _limit(request: Request, kind: str):
    ip = (request.headers.get("x-forwarded-for") or request.client.host or "?").split(",")[0].strip()
    n, window = LIMITS[kind]
    q = _hits[(kind, ip)]
    now = time.time()
    while q and now - q[0] > window:
        q.popleft()
    if len(q) >= n:
        wait = int(window - (now - q[0])) // 60 + 1
        raise HTTPException(429, f"وصلت للحد المسموح. حاول بعد {wait} دقيقة.")
    q.append(now)


def _chat(system: str, user: str, max_tokens: int = 900) -> str:
    out = _client().chat_completion(
        model=LLM_MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        max_tokens=max_tokens,
        temperature=0.3,
    )
    return out.choices[0].message.content.strip()


# ---------------------------------------------------------------- الصور
STYLES = {
    "واقعي": "photorealistic, natural lighting, high detail",
    "رسم زيتي": "oil painting, visible brush strokes, rich colors",
    "كرتوني": "cartoon illustration, clean outlines, vibrant flat colors",
    "ثلاثي الأبعاد": "3D render, soft studio lighting, high detail",
}
SIZES = {"1:1": (1024, 1024), "16:9": (1280, 720), "9:16": (720, 1280)}


class ImageReq(BaseModel):
    prompt: str = Field(min_length=3, max_length=500)
    style: str = "واقعي"
    size: str = "1:1"


def to_english_prompt(text: str, style: str) -> str:
    """يترجم الوصف العربي إلى وصف إنجليزي مناسب لنموذج الصور."""
    if not re.search(r"[؀-ۿ]", text):
        return f"{text}, {STYLES.get(style, '')}"
    en = _chat(
        "You turn Arabic image descriptions into one concise English image-generation prompt. "
        "Output only the prompt, no quotes, no explanation.",
        text,
        max_tokens=120,
    )
    return f"{en}, {STYLES.get(style, '')}"


@app.post("/api/image")
def make_image(req: ImageReq, request: Request):
    _limit(request, "image")
    w, h = SIZES.get(req.size, SIZES["1:1"])
    try:
        prompt = to_english_prompt(req.prompt.strip(), req.style)
        img = _client().text_to_image(prompt, model=IMAGE_MODEL, width=w, height=h)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(502, f"فشل توليد الصورة: {str(e)[:160]}")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=88)
    return {"image": "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), "prompt": prompt}


# ---------------------------------------------------------------- التلخيص
_YT_ID = re.compile(r"(?:v=|youtu\.be/|/shorts/|/embed/|/live/)([A-Za-z0-9_-]{11})")
LENGTHS = {"قصير": "5 bullet points", "متوسط": "10 bullet points", "مفصل": "a detailed summary with headings"}
LANGS = {"العربية": "Arabic", "English": "English", "Français": "French"}
MAX_CHARS = 24000  # حوالي 30-40 دقيقة من الكلام


class SumReq(BaseModel):
    url: Optional[str] = None
    transcript: Optional[str] = Field(default=None, max_length=60000)
    length: str = "قصير"
    lang: str = "العربية"


def video_id(url: str) -> str:
    m = _YT_ID.search(url or "")
    if not m:
        raise HTTPException(400, "الرابط غير صالح. استخدم رابط يوتيوب كاملاً.")
    return m.group(1)


def fetch_transcript(vid: str) -> str:
    from youtube_transcript_api import YouTubeTranscriptApi
    try:
        t = YouTubeTranscriptApi().fetch(vid, languages=["ar", "en", "fr", "es"])
        return " ".join(s.text for s in t)
    except Exception as e:
        raise HTTPException(
            422,
            "تعذّر جلب نص الفيديو (قد لا يملك ترجمة، أو يحجب يوتيوب عناوين الخادم). "
            "الصق نص الفيديو في الخانة الثانية بدلاً من الرابط.",
        ) from e


def summarize_text(text: str, length_label: str, lang_label: str) -> str:
    text = re.sub(r"\s+", " ", text)[:MAX_CHARS]
    key = re.sub(r"[\u064B-\u0652]", "", length_label).split(" ")[0]
    length = LENGTHS.get(key, LENGTHS["قصير"])
    lang = LANGS.get(lang_label, "Arabic")
    return _chat(
        f"You summarize texts and video transcripts. Write in {lang}. Output {length}. "
        "Use only what the text says. Do not invent facts. Start with a one-line title.",
        text,
        max_tokens=1100,
    )


@app.post("/api/summarize")
def summarize(req: SumReq, request: Request):
    _limit(request, "summarize")
    text = (req.transcript or "").strip()
    if not text:
        text = fetch_transcript(video_id(req.url or ""))
    if len(text) < 200:
        raise HTTPException(400, "النص قصير جداً للتلخيص.")
    try:
        summary = summarize_text(text, req.length, req.lang)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(502, f"فشل التلخيص: {str(e)[:160]}")
    return {"summary": summary, "chars": min(len(text), MAX_CHARS)}


@app.get("/api/health")
def health():
    return {"ok": True, "configured": bool(HF_TOKEN)}


# ---------------------------------------------------------------- الصوت
TTS_VOICES = {
    "ar-DZ-IsmaelNeural": "عربي جزائري · إسماعيل (رجل)",
    "ar-DZ-AminaNeural": "عربي جزائري · أمينة (امرأة)",
    "ar-SA-HamedNeural": "عربي سعودي · حامد (رجل)",
    "ar-SA-ZariyahNeural": "عربي سعودي · زارية (امرأة)",
    "ar-EG-SalmaNeural": "عربي مصري · سلمى (امرأة)",
    "ar-EG-ShakirNeural": "عربي مصري · شاكر (رجل)",
    "fr-FR-DeniseNeural": "Français · Denise",
    "en-US-AriaNeural": "English · Aria",
}


class TtsReq(BaseModel):
    text: str = Field(min_length=1, max_length=3000)
    voice: str = "ar-DZ-IsmaelNeural"
    rate: float = 1.0
    pitch: float = 1.0


@app.get("/api/tts/voices")
def tts_voices():
    return [{"id": k, "name": v} for k, v in TTS_VOICES.items()]


@app.post("/api/tts")
async def tts(req: TtsReq, request: Request):
    _limit(request, "tts")
    if req.voice not in TTS_VOICES:
        raise HTTPException(400, "صوت غير معروف.")
    text = req.text.strip()
    if not text:
        raise HTTPException(400, "اكتب نصاً أولاً.")
    rate = max(-50, min(60, round((req.rate - 1) * 100)))
    pitch = max(-30, min(30, round((req.pitch - 1) * 50)))
    try:
        import edge_tts
        comm = edge_tts.Communicate(text, req.voice, rate=f"{rate:+d}%", pitch=f"{pitch:+d}Hz")
        audio = b""
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                audio += chunk["data"]
    except Exception as e:
        raise HTTPException(502, "تعذّر توليد الصوت من الخادم. جرّب صوت الجهاز من القائمة.") from e
    if not audio:
        raise HTTPException(502, "لم يصل صوت من الخادم. جرّب صوت الجهاز من القائمة.")
    return Response(audio, media_type="audio/mpeg")


# ---------------------------------------------------------------- أدوات النص
TEXT_PROMPTS = {
    "tashkeel": ("Add full Arabic diacritics (tashkeel) to the user's text. Do not add, remove or change any word. "
                 "Output only the diacritized text.", 2000),
    "proofread": ("Correct spelling, grammar and punctuation in the user's Arabic text. Keep the wording, tone and meaning; "
                  "change only what is wrong. Output only the corrected text.", 3000),
}


class TextReq(BaseModel):
    mode: str
    text: str = Field(min_length=3, max_length=12000)
    length: str = "قصير"
    lang: str = "العربية"


@app.post("/api/text")
def text_tool(req: TextReq, request: Request):
    _limit(request, "text")
    text = req.text.strip()
    try:
        if req.mode in TEXT_PROMPTS:
            system, cap = TEXT_PROMPTS[req.mode]
            if len(text) > cap:
                raise HTTPException(400, f"النص أطول من {cap} حرفاً.")
            return {"result": _chat(system, text, max_tokens=3500)}
        if req.mode == "summarize":
            if len(text) < 200:
                raise HTTPException(400, "النص قصير جداً للتلخيص.")
            return {"result": summarize_text(text, req.length, req.lang)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(502, f"فشلت المعالجة: {str(e)[:160]}")
    raise HTTPException(400, "أداة غير معروفة.")


# ---------------------------------------------------------------- الصفحات
def _base(request: Request) -> str:
    return (os.getenv("SITE_URL") or str(request.base_url)).rstrip("/")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return pages.home(_base(request))


@app.get("/tools/{slug}", response_class=HTMLResponse)
def tool(slug: str, request: Request):
    t = pages.BY_SLUG.get(slug)
    if not t:
        raise HTTPException(404, "الصفحة غير موجودة")
    return pages.tool_page(t, _base(request))


@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return pages.about(_base(request))


@app.get("/privacy", response_class=HTMLResponse)
def privacy(request: Request):
    return pages.privacy(_base(request))


@app.get("/contact", response_class=HTMLResponse)
def contact(request: Request):
    return pages.contact(_base(request))


@app.get("/sitemap.xml")
def sitemap(request: Request):
    return Response(pages.sitemap(_base(request)), media_type="application/xml")


@app.get("/robots.txt", response_class=PlainTextResponse)
def robots(request: Request):
    return f"User-agent: *\nAllow: /\nDisallow: /api/\nSitemap: {_base(request)}/sitemap.xml\n"


@app.get("/ads.txt", response_class=PlainTextResponse)
def ads_txt():
    pub = pages.ADSENSE_CLIENT.replace("ca-", "")
    if not pub:
        raise HTTPException(404)
    return f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n"


app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
