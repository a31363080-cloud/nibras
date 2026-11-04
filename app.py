(function () {
  function $(id) { return document.getElementById(id); }

  function post(path, body) {
    return fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
      .then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (j) {
          if (!r.ok) throw new Error(typeof j.detail === 'string' ? j.detail : 'حدث خطأ. حاول مرة أخرى.');
          return j;
        });
      });
  }
  function busy(btn, st, on, txt) { btn.disabled = on; st.textContent = on ? txt : ''; }
  function copy(text, btn) {
    var done = function () { var o = btn.textContent; btn.textContent = 'تم النسخ'; setTimeout(function () { btn.textContent = o; }, 1500); };
    try { navigator.clipboard.writeText(text).then(done, function () {}); } catch (e) {}
  }

  // ---------- الوضع الليلي
  var themeBtn = $('theme');
  if (themeBtn) themeBtn.addEventListener('click', function () {
    var root = document.documentElement, cur = root.getAttribute('data-theme');
    if (!cur) cur = window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    var next = cur === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('nibras-theme', next); } catch (e) {}
  });

  // ---------- نص إلى صوت (أصوات الموقع + أصوات الجهاز)
  if ($('txt')) {
    var txt = $('txt'), cnt = $('cnt'), sel = $('voice'), rate = $('rate'), pitch = $('pitch'),
        note = $('ttsNote'), st = $('tts-st'), synth = window.speechSynthesis, devVoices = [], audio = null, audioUrl = null;
    var upd = function () { cnt.textContent = txt.value.length; };
    txt.addEventListener('input', upd); upd();
    rate.addEventListener('input', function () { $('rv').textContent = (+rate.value).toFixed(1); });
    pitch.addEventListener('input', function () { $('pv').textContent = (+pitch.value).toFixed(1); });
    var msg = function (t, ok) { note.hidden = !t; note.textContent = t || ''; note.className = 'note' + (ok ? ' ok' : ''); };

    function fill(server) {
      sel.innerHTML = '';
      var g1 = document.createElement('optgroup'); g1.label = 'أصوات الموقع (تعمل على كل الأجهزة)';
      server.forEach(function (v) { var o = document.createElement('option'); o.value = 'srv:' + v.id; o.textContent = v.name; g1.appendChild(o); });
      if (server.length) sel.appendChild(g1);
      if (synth) {
        var all = synth.getVoices();
        var ar = all.filter(function (v) { return /^ar/i.test(v.lang); });
        devVoices = ar.length ? ar : all;
        var g2 = document.createElement('optgroup'); g2.label = 'أصوات جهازك' + (ar.length ? '' : ' (بلا عربية)');
        devVoices.forEach(function (v, i) { var o = document.createElement('option'); o.value = 'dev:' + i; o.textContent = v.name + ' (' + v.lang + ')'; g2.appendChild(o); });
        if (devVoices.length) sel.appendChild(g2);
      }
    }
    var serverVoices = [];
    fetch('/api/tts/voices').then(function (r) { return r.ok ? r.json() : []; }).catch(function () { return []; })
      .then(function (v) { serverVoices = v; fill(serverVoices); if (!v.length && synth) msg('تعذّر تحميل أصوات الموقع، استخدم صوت جهازك.'); });
    if (synth) synth.onvoiceschanged = function () { var cur = sel.value; fill(serverVoices); if (cur) sel.value = cur; };

    function stopAll() {
      if (synth) synth.cancel();
      if (audio) { audio.pause(); audio = null; }
      if (audioUrl) { URL.revokeObjectURL(audioUrl); audioUrl = null; }
    }
    $('play').addEventListener('click', function () {
      if (audio && audio.paused && audio.currentTime > 0 && !audio.ended) { audio.play(); return; }
      if (synth && synth.paused) { synth.resume(); return; }
      stopAll(); msg('');
      var t = txt.value.trim(); if (!t) { msg('اكتب نصاً أولاً.'); return; }
      var val = sel.value || '';
      if (val.indexOf('srv:') === 0) {
        var btn = $('play'); btn.disabled = true; st.textContent = 'جارٍ تجهيز الصوت...';
        fetch('/api/tts', { method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: t, voice: val.slice(4), rate: +rate.value, pitch: +pitch.value }) })
          .then(function (r) {
            if (!r.ok) return r.json().catch(function () { return {}; }).then(function (j) { throw new Error(typeof j.detail === 'string' ? j.detail : 'تعذّر توليد الصوت.'); });
            return r.blob();
          })
          .then(function (b) { audioUrl = URL.createObjectURL(b); audio = new Audio(audioUrl); return audio.play(); })
          .catch(function (e) { msg(e && /[\u0600-\u06FF]/.test(e.message || '') ? e.message : 'تعذّر تشغيل الصوت. جرّب صوتاً آخر.'); })
          .then(function () { btn.disabled = false; st.textContent = ''; });
        return;
      }
      if (!synth) { msg('هذا المتصفح لا يدعم أصوات الجهاز. اختر أحد أصوات الموقع.'); return; }
      var u = new SpeechSynthesisUtterance(t);
      var v = devVoices[+val.slice(4)]; if (v) { u.voice = v; u.lang = v.lang; } else u.lang = 'ar-SA';
      u.rate = +rate.value; u.pitch = +pitch.value;
      u.onerror = function () { msg('تعذّر التشغيل. جرّب صوتاً آخر.'); };
      synth.speak(u);
    });
    $('pause').addEventListener('click', function () { if (audio) audio.pause(); if (synth) synth.pause(); });
    $('stop').addEventListener('click', stopAll);
  }

  // ---------- توليد الصور
  if ($('igo')) {
    document.querySelectorAll('#styles button').forEach(function (b) {
      b.addEventListener('click', function () {
        document.querySelectorAll('#styles button').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', 'true');
      });
    });
    var igo = $('igo');
    igo.addEventListener('click', function () {
      var err = $('ierr'), res = $('ires');
      var style = document.querySelector('#styles button[aria-pressed="true"]').textContent;
      var size = $('size').value.split(' ')[1] || '1:1';
      err.hidden = true; res.hidden = true; busy(igo, $('ist'), true, 'جارٍ التوليد، قد يستغرق دقيقة...');
      post('/api/image', { prompt: $('ip').value, style: style, size: size }).then(function (j) {
        $('iimg').src = j.image; $('idl').href = j.image; res.hidden = false;
      }).catch(function (e) { err.textContent = e.message; err.hidden = false; })
        .then(function () { busy(igo, $('ist'), false); });
    });
  }

  // ---------- تلخيص الفيديو
  if ($('vgo')) {
    var vgo = $('vgo');
    vgo.addEventListener('click', function () {
      var err = $('verr'), res = $('vres');
      var t = $('vt').value.trim(), u = $('vu').value.trim();
      if (!t && !u) { err.textContent = 'ضع رابط فيديو أو الصق نصه.'; err.hidden = false; return; }
      err.hidden = true; res.hidden = true; busy(vgo, $('vst'), true, 'جارٍ التلخيص...');
      post('/api/summarize', { url: u || null, transcript: t || null, length: $('vl').value, lang: $('vo').value }).then(function (j) {
        $('vsum').textContent = j.summary; res.hidden = false;
      }).catch(function (e) { err.textContent = e.message; err.hidden = false; })
        .then(function () { busy(vgo, $('vst'), false); });
    });
    $('vcopy').addEventListener('click', function () { copy($('vsum').textContent, $('vcopy')); });
  }

  // ---------- أدوات النص (تشكيل / تدقيق / تلخيص)
  if ($('tgo')) {
    var mode = $('text').dataset.mode, tx = $('tx'), tgo = $('tgo');
    var tu = function () { $('tcnt').textContent = tx.value.length; };
    tx.addEventListener('input', tu); tu();
    tgo.addEventListener('click', function () {
      var err = $('terr'), res = $('tres');
      if (tx.value.trim().length < 3) { err.textContent = 'الصق نصاً أولاً.'; err.hidden = false; return; }
      err.hidden = true; res.hidden = true; busy(tgo, $('tst'), true, 'جارٍ المعالجة...');
      post('/api/text', {
        mode: mode, text: tx.value,
        length: $('tl') ? $('tl').value : 'قصير', lang: $('to') ? $('to').value : 'العربية'
      }).then(function (j) { $('tout').textContent = j.result; res.hidden = false; })
        .catch(function (e) { err.textContent = e.message; err.hidden = false; })
        .then(function () { busy(tgo, $('tst'), false); });
    });
    $('tcopy').addEventListener('click', function () { copy($('tout').textContent, $('tcopy')); });
  }
})();
