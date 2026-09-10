# Step 6 — Landing Generation + Step 7a-c — Polish Layer 


**Объединяет:** Step 6 (сборка лендинга) + Step 7a (SEO/GEO) + Step 7b (Mobile) + Step 7c (PageSpeed). **Step 7d (Multilingual)** — отдельный блок: в исходном репозитории `../07-polish/multilingual-single-file.md`, после установки `../landing-polish/multilingual-single-file.md`.

---

## 0. Назначение блока

Шестой и седьмой шаги pipeline — самые объёмные. Council (в роли **Landing Generator**, затем **Polish Layer** с sub-ролями SEO / Mobile / Performance) собирает полноценный лендинг и доводит его до готового к деплою состояния.

**Входные данные:**
- Discovery Brief (Шаг 1) — тип продукта, регион (legal-требования), язык, стек
- Reviews Synthesis (Шаг 2) — опц.
- Custdev Synthesis (Шаг 3) — primary сегмент, барьеры и мотивы из 10 симулированных персон; всё остаётся явно помеченными гипотезами
- Copy Brief (Шаг 4) — финальный копирайт
- Design choice (Шаг 5) — `design-tokens.json` + `component-library.md` + выбранный стиль

**Выход:**
- Файлы лендинга в выбранном стеке (HTML / TSX / Vue / Svelte / Framer / Webflow)
- `images/` — placeholders с осмысленными именами
- `stack-choice-rationale.md` — 2 строки почему этот стек
- `pagespeed-analysis.md` — отчёт Polish Layer с auto-fix применён
- `visual-content-suggestions.md` — что юзеру доделать руками
- Готовый лендинг — проходит pre-flight checklist из LANDING-RULES

**Принцип:** один шаг = одна большая сборка с последовательными sub-ролями. Юзер видит промежуточные результаты после 6a (landing pattern) → 6b (структура) → 6c (код) → 7a (SEO/GEO) → 7b (mobile) → 7c (PageSpeed). Между sub-ролями — короткие паузы, юзер может прервать.

---

## 1. Step 6 — Landing Generation

### 1.1 Приветствие

> Шаг 6 из 7 — Landing Generation. Сейчас я (в роли Landing Generator) возьму всё, что мы собрали, и соберу рабочий лендинг одним махом:
>
> 1. **Подбираю landing pattern** из 34 (по Copy Brief, сегменту, стилю)
> 2. **Фиксирую структуру секций** — под твои value props, возражения, social proof
> 3. **Выбираю стек** и собираю код (HTML+Tailwind / Next.js+shadcn / Astro+MDX / Framer / Webflow)
> 4. **Применяю критические правила** — Hero на primary barrier, no base64, WebP, anti-AI-slop
>
> Всё это — одним output'ом, без пауз между под-этапами. После меня пройдёт Polish Layer (SEO/GEO + Mobile в одной сборке, потом PageSpeed отдельно — для него нужна твоя деплой-проверка).
>
> Это самый большой шаг по объёму. Код пойдёт в артефакт / Canvas, чтобы не есть чат. Поехали?

### 1.2 Этап 6a — подбор landing pattern

Council выбирает один из 34 patterns в `landing.csv` по критериям:
- **Цель лендинга** (Discovery) — waitlist / lead gen / прямая продажа / demo request
- **Наличие social proof в Copy Brief** — если testimonials есть или в [FILL: waitlist count] — pattern с соответствующей секцией
- **Количество value props** из Copy Brief — 3 блока = короче pattern, 5 блоков = длиннее
- **Количество возражений** из Copy Brief — 3 возражения интегрируются инлайн, 5+ требуют отдельного FAQ
- **Выбранный стиль** (Шаг 5) — некоторые patterns не работают с определёнными стилями (например, «Hero + long story scroll» не подходит к brutalism)

Output этапа 6a:

```markdown
## Landing Pattern: «{название из landing.csv}»

**Почему этот:** {2 строки — связка с Copy Brief + стилем}
**Section order:** {список секций одной строкой}
**CTA placement:** {из landing.csv + адаптация под длину лендинга}
**Color strategy:** {из landing.csv, адаптировано под выбранную палитру}
**Recommended effects:** {из landing.csv, адаптировано под выбранный стиль}
```

Без паузы — идём дальше.

### 1.3 Этап 6b — финальная структура секций

Council разворачивает pattern в конкретные секции с привязкой к Copy Brief:

```markdown
## Финальная структура

1. **Hero**
   - H1: {финальный H1 из Copy Brief — выбранный в Шаге 5 при 3-вариантах, либо рекомендованный}
   - Sub-head: {финальный}
   - CTA: {финальный}
   - Визуал: {из Copy Brief visual direction}

2. **{секция 2}**
   - Тип: value prop / social proof / objection / pricing / FAQ / ...
   - Контент: {ссылка на блок из Copy Brief — например, «value prop #1: "..."»}
   - Social proof: если есть — заполнено, если нет — `[FILL: ...]` с инструкцией

[и так далее — каждая секция + привязка к Copy Brief]

N. **Footer**
   - Legal ссылки: {состав из Discovery по региону}
   - Копирайт: {автогенерация года}
   - Контакты: {из Discovery}
```

Без паузы — идём в 6c (юзер правит постфактум, единым запросом после всего output'а).

### 1.4 Этап 6c — автовыбор стека и генерация кода

Council выбирает стек (**не спрашивает юзера**, говорит что выбрал и почему в 2 строки):

- **Simple marketing landing** → HTML + Tailwind
- **Interactive landing + форма** → Next.js + shadcn/ui
- **Visual-heavy, no-code** → Framer или Webflow (если Discovery показал «не умею кодить» или «предпочитаю визуальные редакторы»)
- **Portfolio / blog integration** → Astro + MDX
- **App landing + dashboard integration** → inherit стек приложения

Если юзер в Discovery указал конкретный стек — Council уважает выбор и пишет: «Ты указал {стек}, использую его».

**Статус-маркер** (один, редкий): `→ генерирую код ({стек})`.

Output — файлы лендинга в формате стека. Для HTML+Tailwind — один `index.html` с inline CSS/JS; для Next.js — `app/page.tsx` + компоненты; для Framer/Webflow — инструкция какие блоки поставить.

**КРИТИЧЕСКИЕ ПРАВИЛА генерации:**

**Правило #1 — Hero на primary barrier.** H1 отвечает на primary barrier из проверяемых Reviews Synthesis или на явно помеченную гипотезу Custdev Synthesis. Формула «[Outcome] + [despite barrier]» или «[Barrier removal] + [outcome]». H1 тег обязателен (SEO). Длина 5-10 слов (одна строка desktop).

**Правило #2 — никогда base64.** Изображения = локальные файлы `/images/{имя}.webp` или внешний CDN. Council спрашивает юзера:
> Куда положим картинки: (A) в репо в папку `/images/`, (B) внешний CDN (Cloudinary / S3)?

**Правило #3 — WebP обязательно.** Council даёт инструкцию:
> Конвертируй свои картинки в WebP через [squoosh.app](https://squoosh.app). Имена файлов — осмысленные: `hero.webp`, `product_screenshot.webp`, не `DSC00123.jpg`. В HTML использую `<picture>` с fallback на JPEG.

**Правило #4 — anti-AI-slop фильтр.** Всё, что прошло в Copy Brief, уже очищено от запрещённых фраз. В коде Council дополнительно проверяет: никаких эмодзи, никаких «revolutionary», никаких floating UI-cards SaaS-стиля 2022, никаких purple-to-blue gradients, никаких stack icons row.

**Правило #5 — формы.** Default pattern: HTML form → Google Apps Script (`doPost`) → Google Sheets. Council встраивает форму, даёт пустой `endpoint` с пометкой `[FILL: Apps Script URL]` + инструкцию (6 шагов: создать таблицу → Extensions → Apps Script → вставить скрипт → Deploy → Web app → Anyone access → скопировать URL → вставить в `form action`).

**Правило #6 — footer и legal.** Копирайт с автогенерацией года (`<span id="year"></span>` + JS). Legal-ссылки по региону (privacy / terms / cookies — состав определяется Discovery-ответом про регион: CCPA для California, GDPR для EU, PDPA для Singapore, PIPL для China, российский 152-ФЗ и т.д.).

Council **сам генерирует legal-документы** (`privacy.html`, `terms.html`, `cookies.html`) с нужным составом блоков под регион и тип продукта. Показывает юзеру предупреждение:

> Это черновики legal-документов, а не юридическая консультация. До запуска проверь фактические процессы обработки данных, используемые cookies/пиксели, подрядчиков и требования конкретных стран. Для платежей, здоровья, детей, биометрии и других чувствительных данных нужна профильная юридическая проверка. Не публикуй шаблон, пока все `[FILL: …]` не заполнены и не подтверждены владельцем продукта.

**Правило #7 — структура.** Только Hero и Footer обязательны. Остальные секции — по необходимости (Правило 8 из LANDING-RULES-UNIVERSAL). Длина определяется проверяемыми сигналами, задачей лендинга и доступными доказательствами.

### 1.5 Output Step 6

```
/{project}/
├── index.html (или app/page.tsx в зависимости от стека)
├── [privacy.html, terms.html, cookies.html] — если применимо к региону
├── images/
│   └── [placeholders с осмысленными именами]
├── stack-choice-rationale.md — 2 строки «стек выбран потому что ...»
└── — всё готово к Step 7 (Polish Layer)
```

### 1.6 Размер output

Код лендинга может быть большим (5-15 тысяч слов для HTML, меньше для Next.js потому что компоненты). Council выгружает:

- **Claude:** код идёт в **артефакт** (type: `text/html` для простого HTML, `application/vnd.ant.react` для React). Один артефакт на один файл. Основной чат остаётся чистым
- **ChatGPT:** код идёт в **Canvas**
- **Gemini:** **Canvas**
- **Perplexity / другие:** код в чат с пометкой «большой блок, следующие шаги могут упереться в лимит». Совет: после копирования в файл — открыть новый чат для Polish Layer, скопировав туда Copy Brief + design-tokens + финальный код

---

## 2. Step 7a + 7b — SEO/GEO + Mobile (одной сборкой)

### 2.1 Приветствие

> Step 7 — Polish Layer. Делаю SEO/GEO оптимизацию и мобильную адаптацию за один проход — это code-fixes без твоих действий. После сразу перейдём к PageSpeed (там нужен деплой + проверка от тебя).

### 2.2 Что делает Council

**Keyword research:** 1 primary keyword + 3-5 long-tail. Source — Discovery Brief (тип продукта, регион, язык) + vocabulary из Reviews Synthesis + явно помеченные мотивы-гипотезы из Custdev Synthesis.

**Meta tags:**
- `<title>` — 55-60 символов, содержит primary keyword, не перегружен
- `<meta description>` — 150-160 символов, содержит primary motivator из Copy Brief

**Open Graph + Twitter Card:**
- `og:title`, `og:description`, `og:image` (1200×630; PNG/JPEG для широкой совместимости с мессенджерами)
- `twitter:card="summary_large_image"`
- `og:image` — placeholder `[FILL: og-image.jpg]` с инструкцией

**Schema.org JSON-LD** (по типу продукта):
- `WebPage` / `Product` / `SoftwareApplication` / `Service` / `Course` / etc.
- `Organization` или `Person` (из Discovery)
- `FAQPage` — если FAQ есть в лендинге
- `BreadcrumbList` — если лендинг часть сайта
- `Review` + `AggregateRating` — если social proof с рейтингами есть

**GEO-слой (AI-search оптимизация):**
- `speakable` не добавлять на обычный лендинг: это ограниченный beta-сценарий, не универсальный GEO-сигнал
- **HowTo schema** — только если есть видимая пошаговая инструкция; не обещать rich result
- **FAQPage** — только если FAQ видим на странице; не обещать rich result
- **First paragraph Hero** — прямой ответ на primary query (для AI-extraction)
- `llms.txt` — опциональный экспериментальный навигационный файл, не подтверждённый фактор ранжирования или цитирования

### 2.3 Что ещё делает Council (Mobile sub-role — тот же проход)

**Breakpoints:**
- 375px (iPhone baseline) — основной
- 768px (планшет)
- 1024px+ (desktop)

**Mobile-first подход** — стили пишутся под мобильный как default, desktop — через `@media (min-width: ...)`. Если в Шаге 6 было иначе (desktop-first) — Council рефакторит.

**Touch targets:** все кнопки, ссылки, поля формы — минимум 44×44px (iOS HIG).

**Typography scaling:** variable font sizes через `clamp()` или breakpoint-specific.

**Responsive images:** `<picture>` + `srcset` + `sizes` для разных разрешений.

**Core Web Vitals — проверяет правилами:**
- LCP < 2.5s: hero image preload, шрифты через `font-display: swap`
- INP < 200ms: нет тяжёлого JS в critical path
- CLS < 0.1: у всех изображений `width`/`height`, шрифты без FOIT

**Accessibility:**
- semantic HTML (`<header>`, `<main>`, `<section>`, `<footer>`, `<nav>`, `<article>`)
- `alt` на всех изображениях (placeholder `[FILL: alt text]` если юзер не дал)
- contrast ratio 4.5:1+ (для обычного текста) и 3:1+ (для крупного) — проверяется против палитры из Шага 5
- keyboard navigation — focus states на всех интерактивных элементах

### 2.4 Output 7a+7b одной сборкой

Обновлённые файлы (SEO patches в `<head>` + schema.org блоки + mobile CSS патчи + accessibility fixes). Не перегенерируем файл целиком — только diff. В Claude/ChatGPT/Gemini патч показывается в артефакте / Canvas.

Короткая пауза перед 7c — юзер читает diff, говорит «продолжай к PageSpeed» или «поправь X в SEO / mobile».

---

## 3. Step 7c — PageSpeed sub-role

### 3.1 Приветствие + инструкция юзеру

> Step 7c — PageSpeed Insights. Нужен твой деплой + одна проверка. Вот что делаешь:
>
> 1. **Деплой лендинга** — любая из 5 платформ (Vercel / Netlify / Framer / Webflow / self-hosted). Инструкции по деплою — в `DEPLOY.md`
> 2. Открой **[pagespeed.web.dev](https://pagespeed.web.dev)**
> 3. Вставь URL задеплоенного лендинга → дождись отчёт (Mobile + Desktop, ~30 сек)
> 4. **Скопируй весь отчёт сюда одним сообщением** — я разберу и применю fixes
>
> Делаем одну проверку (после применения fixes повторный прогон уже на твоё усмотрение — обычно не нужен). Жду отчёт.

### 3.2 После получения отчёта

Council парсит:
- **Performance score** (0-100) — Mobile + Desktop
- **Core Web Vitals** — LCP, INP, CLS
- **Opportunities** — unused CSS/JS, image format suggestions, text compression, render-blocking
- **Diagnostics** — остальное

Классифицирует проблемы на 2 группы:

**Technical fixes (auto-apply):**
- Unused CSS → remove
- Missing compression headers → добавить в deploy config
- Missing `loading="lazy"` на below-fold images
- Missing `width`/`height` на изображениях
- Render-blocking resources → `defer` / `async`
- Missing meta / alt — patched
- Inline critical CSS — inline если не было

Council применяет все technical fixes, **показывает список изменений одной строкой каждое**:
```
Применил:
- Добавил loading="lazy" на 4 изображения ниже fold
- Убрал 12KB неиспользуемого CSS (секция .card-floating — не используется)
- Добавил defer к analytics script
- [остальные fixes...]
```

**Visual/content fixes (ASK user):**
- «Замени hero.jpg на WebP — сэкономит 180KB. Используй squoosh.app»
- «Сократи hero sub-head с 2 строк до 1 — мобильный CLS на 0.02 улучшится»
- «Удали секцию X — она не даёт конверсий по heatmap-тестам (gen. рекомендация, не факт)»

Council перечисляет — юзер делает руками (или говорит «примени рекомендацию #N»).

### 3.3 Повторная проверка — по желанию юзера

Council говорит:
> Fixes применены. Если хочешь подтвердить — прогони PSI ещё раз и пришли отчёт, я сравню до/после одной строкой. Если нет — считаю работу завершённой.

Типичный сценарий — юзер не гоняет второй раз, принимает fixes «на веру». Council не настаивает.

Если второй прогон был → Council показывает сводку:
> Performance Mobile: 68 → 92 (+24). LCP: 3.2s → 2.1s. CLS: 0.18 → 0.05. INP: 240ms → 120ms. Готово к запуску.

### 3.4 Output Step 7c

- `pagespeed-analysis.md` — разбор с классификацией и списком применённых fixes
- Обновлённые файлы лендинга (после auto-fix)
- `visual-content-suggestions.md` — что сделать руками

---

## 4. Сохранение и статус

> Сохрани артефакты этого шага в папку проекта и отметь шаг в `STATUS.md` (шаблон — `project-template/`).

## 5. Учёт предыдущих шагов

### 6.1 Если Discovery отметил регион
- Legal-ссылки в footer = состав по региону (privacy / terms / cookies / + региональные: CCPA / GDPR / PDPA / PIPL / 152-ФЗ)
- Consent/opt-out определяется по региону и реальным технологиям: для EU/UK несущественные cookies обычно блокируются до согласия; для California отдельно проверяются disclosure, opt-out sale/share и Global Privacy Control

### 6.2 Если Copy Brief отметил мультиязычность
- Step 6 делает primary язык из Discovery
- После Step 7c — переход в **Step 7d (Multilingual)** по файлу `07-polish/multilingual-single-file.md`
- Multilingual — ТОЛЬКО в самом конце, после утверждённого финального EN (или другого primary) лендинга. Причина: LLM галлюцинирует при переводе во время разработки

### 6.3 Если гипотезы Custdev Synthesis не проверены
- В финальный чек-лист добавляется пометка: «Эти формулировки основаны на непроверенных гипотезах; дизайн и A/B-тест не заменяют проверку живыми источниками или пользователями»

### 6.4 Если Copy Brief оставил `[FILL: ...]` placeholders
Council в финальном отчёте перечисляет все оставшиеся `[FILL: ...]` одним списком:
> Осталось заполнить до запуска:
> - [FILL: og-image.jpg 1200×630] — сделай в Canva / Figma
> - [FILL: hero.webp] — конвертируй через squoosh.app
> - [FILL: 3 testimonials с фото] — собери до запуска
> - [FILL: Apps Script endpoint] — по инструкции в `DEPLOY.md` (раздел «Формы»)
> - [FILL: alt text для изображений] — дай мне альтов, я встрою

---

## 6. Переход к Step 7d (Multilingual) или завершение

### 7.1 Если мультиязычность нужна
> Полный лендинг на {primary language} готов. Финализируй и утверди — дальше делаем переводы.
>
> Когда готов — напиши «утверждаю» или «запускай перевод», я подниму файл `07-polish/multilingual-single-file.md` и начну Step 7d.

### 7.2 Если мультиязычность не нужна
> Pipeline завершён. У тебя на руках полноценный лендинг, готовый к деплою:
> - Код в твоём стеке ({стек})
> - SEO/GEO метаданные и schema.org разметка
> - Mobile-адаптация
> - PageSpeed оптимизация (score {N} Mobile / {N} Desktop)
> - Список `[FILL: ...]` что доделать руками
>
> Следующий шаг — деплой и валидация на живых пользователях. Инструкции по деплою (5 платформ на выбор) — в `DEPLOY.md`.

---

## 7. Оптимизация токенов

- Код лендинга идёт в артефакт / Canvas — не ест контекст основного чата (Claude / ChatGPT / Gemini)
- Patches после 7a / 7b / 7c — это diffs, не полные перегенерации файлов
- Каждый fix в 7c описывается одной строкой, не развёрнутым абзацем
- Статус-маркеры редкие (только на тяжёлых операциях)
- При больших отчётах PSI — парсинг результата происходит внутри, юзеру выводится только сводка + классификация
- `[FILL: ...]` собираются в один финальный список, не раскиданы по документу

---
