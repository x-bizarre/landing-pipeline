# Multilingual Static Site — Single-File Architecture

**Применяется:** Step 7d (Multilingual, последний шаг после утверждения финальной EN-версии).

**Принцип:** один HTML-файл на страницу, переключение языка через JS + `localStorage`, без серверной логики, без URL-префиксов. Работает на Vercel / GitHub Pages / Netlify.

---

## Core Principles

1. **Один HTML-файл на страницу** — без дубликатов страниц per language
2. **URL не меняется** — один URL для всех языков
3. **Auto-detection** — язык определяется через `navigator.language` при первом визите
4. **User override** — language switcher в nav, выбор сохраняется в `localStorage`
5. **Cross-page sync** — все страницы читают один `localStorage` key → переключение на одной странице сохраняется на других

---

## 1. HTML Markup — `data-i18n` Attributes

Каждый переводимый элемент получает `data-i18n` с уникальным ключом. Default (EN) остаётся как innerHTML для SEO и no-JS fallback.

```html
<h1 data-i18n="hero_title">Your team designs albums <em>in hours.</em></h1>
<p data-i18n="hero_sub">Upload photos, get a print-ready album.</p>
```

Для `placeholder` атрибутов:

```html
<input type="text" data-i18n-placeholder="form_name" placeholder="Your name" required>
```

Для `<select>` элементов (options обновляются программно через `setLang()`, т.к. `innerHTML` replacement ломает структуру):

```html
<select id="demo-interest" required>
  <option value="" data-i18n="form_interest">I'm interested in...</option>
  <option data-i18n="form_opt_back">Back-office tool</option>
  <option data-i18n="form_opt_wl">White-label integration</option>
</select>
```

## 2. Translation Object

Все переводы в едином JS-объекте `T` с кодами языков как keys. Каждый `data-i18n` ключ должен существовать во всех языках.

```javascript
const T = {
  en: {
    hero_title: 'Your team designs albums <em>in hours.</em>',
    hero_sub: 'Upload photos, get a print-ready album.',
    form_name: 'Your name',
    form_interest: "I'm interested in...",
    // ...
  },
  es: {
    hero_title: 'Tu equipo diseña álbumes <em>en horas.</em>',
    hero_sub: 'Sube fotos, obtén un álbum listo para imprimir.',
    form_name: 'Tu nombre',
    form_interest: 'Me interesa...',
    // ...
  },
  pt: {
    hero_title: 'Sua equipe projeta álbuns <em>em horas.</em>',
    hero_sub: 'Envie fotos, receba um álbum pronto para impressão.',
    form_name: 'Seu nome',
    form_interest: 'Tenho interesse em...',
    // ...
  }
};
```

**Правила для ключей:**
- Values могут содержать HTML (`<em>`, `<strong>`, `<a>`) — инжектятся через `innerHTML`
- Используй single quotes когда value содержит double quotes
- Ключи короткие и семантичные: `hero_title`, `feat_ai_text`, `faq_3_q`

## 3. Language Switcher (UI)

Простые кнопки в nav. Активное состояние через `.active` class.

```html
<div class="lang-switcher">
  <button class="lang-btn active" onclick="setLang('en')">EN</button>
  <button class="lang-btn" onclick="setLang('es')">ES</button>
  <button class="lang-btn" onclick="setLang('pt')">PT</button>
</div>
```

```css
.lang-switcher { display: flex; gap: 4px; align-items: center; }
.lang-btn {
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.1);
  color: #A3B1BD;
  padding: 5px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
}
.lang-btn.active {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}
```

## 4. `setLang()` Function

Core-функция применения переводов. Вызывается на клик кнопки и на page load.

```javascript
let currentLang = 'en';
const LANG_KEY = 'site_lang'; // adjust per project with a short prefix, e.g. 'acme_lang'

function setLang(lang) {
  currentLang = lang;
  document.documentElement.lang = lang;
  localStorage.setItem(LANG_KEY, lang);

  // Update switcher buttons
  document.querySelectorAll('.lang-btn').forEach(b =>
    b.classList.toggle('active', b.textContent.trim() === lang.toUpperCase())
  );

  const t = T[lang];

  // Replace innerHTML for all data-i18n elements
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const k = el.getAttribute('data-i18n');
    if (t[k] !== undefined) el.innerHTML = t[k];
  });

  // Replace placeholders
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const k = el.getAttribute('data-i18n-placeholder');
    if (t[k] !== undefined) el.placeholder = t[k];
  });

  // Update select options manually (если есть select)
  const sel = document.getElementById('demo-interest');
  if (sel) {
    sel.options[0].text = t.form_interest;
    sel.options[1].text = t.form_opt_back;
    // ... и так далее для каждой option
  }

  // Re-render dynamic content (carousels, etc.)
  if (typeof renderProducts === 'function') renderProducts();
}
```

## 5. Auto-Detection на page load

Запускается 1 раз при загрузке. Priority: `localStorage` → `navigator.language` → English fallback.

```javascript
(function() {
  const saved = localStorage.getItem(LANG_KEY);
  if (saved && T[saved]) { setLang(saved); return; }

  const browser = (navigator.language || '').toLowerCase();
  if (browser.startsWith('pt')) setLang('pt');
  else if (browser.startsWith('es')) setLang('es');
  else if (browser.startsWith('ru')) setLang('ru');
  else if (browser.startsWith('de')) setLang('de');
  else if (browser.startsWith('fr')) setLang('fr');
  else setLang('en');
})();
```

---

## Patterns для специфичных элементов

### Dynamic Content (JS-rendered)

Для элементов рендерящихся JavaScript'ом (carousels, product cards), переводы применяются внутри render-функции используя `T[currentLang]`:

```javascript
function renderProducts() {
  const t = T[currentLang];
  // Build HTML using t.product_name, t.ar_badge, etc.
}
```

Вызывать `renderProducts()` в конце `setLang()`.

### Pages без dynamic content (Terms, Privacy)

Для простых текстовых страниц — block-level switching вместо `data-i18n`:

```html
<div class="lang-block active" id="lang-en">
  <h1>Terms of Use</h1>
  <p>Full English content here...</p>
</div>
<div class="lang-block" id="lang-es">
  <h1>Términos de Uso</h1>
  <p>Full Spanish content here...</p>
</div>
<div class="lang-block" id="lang-pt">
  <h1>Termos de Uso</h1>
  <p>Full Portuguese content here...</p>
</div>
```

```css
.lang-block { display: none; }
.lang-block.active { display: block; }
```

```javascript
function setLang(lang) {
  document.querySelectorAll('.lang-block').forEach(b => b.classList.remove('active'));
  document.getElementById('lang-' + lang).classList.add('active');
  // ... update switcher, localStorage
}
```

**Когда что использовать:**
- `data-i18n` → страницы с общим layout, формами, интерактивными элементами (landing, roadmap, pricing)
- `lang-block` → страницы pure text без общих interactive элементов (terms, privacy, cookies)

### Animated/Cycling Content

Для typing animations или rotating text — массивы per language:

```javascript
const prompts = {
  en: ['floral watercolor...', 'starry night...', 'kids fairy tale...'],
  es: ['acuarela floral...', 'noche estrellada...', 'cuento infantil...'],
  pt: ['aquarela floral...', 'noite estrelada...', 'conto infantil...']
};

function cyclePrompt() {
  const el = document.getElementById('promptText');
  const arr = prompts[currentLang] || prompts.en;
  el.style.opacity = '0';
  setTimeout(() => {
    el.textContent = arr[idx % arr.length];
    el.style.opacity = '1';
    idx++;
  }, 300);
}
setInterval(cyclePrompt, 2800);
```

---

## Cross-Page Sync

Все страницы share тот же `localStorage` key (например `site_lang`). Когда юзер переключает на Spanish на landing page, потом идёт на Roadmap или Terms — они auto-detect сохранённое preference.

**Required на каждой странице:**
1. Same `localStorage.getItem(LANG_KEY)` check on load
2. Same `localStorage.setItem(LANG_KEY, lang)` on switch
3. Same language switcher UI

---

## SEO Considerations

- Default language (EN) в HTML source → crawlers индексируют его
- `<html lang="en">` обновляется динамически через `document.documentElement.lang = lang`
- `<meta name="description">` остаётся на EN (primary market)
- Canonical/hreflang tags не нужны т.к. один URL per page
- Если SEO для non-English markets становится критичным → переходить на server-side rendering или static generation per language

---

## Чек-лист добавления новой страницы

1. Скопировать `<nav>` с language switcher с любой existing страницы
2. Добавить `data-i18n` атрибуты на все переводимые элементы
3. Создать `T` объект с `en`, `es`, `pt` keys (или импорт shared translations)
4. Добавить `setLang()` функцию и auto-detection IIFE
5. Если форма: скопировать HTML формы, select update logic, submit handler
6. Тест: переключить язык → refresh → язык сохраняется → перейти на другую страницу → сохраняется

## Чек-лист добавления нового языка

1. Добавить кнопку в `.lang-switcher`: `<button class="lang-btn" onclick="setLang('fr')">FR</button>`
2. Добавить `fr: { ... }` в объект `T` на каждой странице со всеми ключами переведёнными
3. Добавить `'fr'` в auto-detection check: `if (browser.startsWith('fr')) setLang('fr');`
4. Для block-level страниц: добавить `<div class="lang-block" id="lang-fr">` с переводом
5. Тест всех страниц, включая form placeholders и select options

---

## Применение в Landing Brief Council (Step 7d)

**Критическое правило:** Step 7d выполняется ТОЛЬКО после утверждения финальной EN-версии. При переводе во время разработки LLM галлюцинирует — теряет ключевые фразы, смешивает tone.

**Flow для Step 7d:**

1. Финальная EN-версия лендинга стабильна, утверждена юзером
2. Multilingual Translator (Council role) применяет эту архитектуру:
   - Добавляет `data-i18n` атрибуты на переводимые элементы
   - Строит `T` объект
   - Добавляет language switcher в nav
   - Имплементирует `setLang()` + auto-detection
3. **При переводе сохранять tone из Copy Brief** — culture-adapt не буквально
4. **НЕ переводить brand names / slogans буквально** — адаптировать смысл
5. **Primary barrier + hero promise** — особенно аккуратно адаптировать под культурный контекст каждого региона
6. **Schema.org markup** обновить на каждом языке (либо через JSON-LD inject в setLang, либо отдельные теги)
