# DEPLOY — как выложить лендинг и подключить форму

Выбери один путь. Условия бесплатных тарифов и интерфейсы провайдеров меняются, поэтому перед запуском проверь их актуальные ограничения.

## Путь A — Vercel CLI или Netlify Drop (без git)

1. Собери папку: `index.html`, legal-страницы, `images/`.
2. Netlify: https://app.netlify.com/drop — перетащи папку, получи URL. Vercel: выполни `npx vercel@latest deploy` для preview, проверь URL, затем `npx vercel@latest deploy --prod`.
3. Для Netlify обновление — повторная загрузка; для Vercel — повторная CLI-команда. Подходит для fakedoor и первых версий.

## Путь B — GitHub + автодеплой (рекомендуется)

1. Создай репозиторий, положи файлы, запушь в `main`.
2. Импортируй репозиторий в Vercel или Netlify. Каждый push в `main` — новый деплой.
3. **Проверь до первого пуша, что интеграция включена:** в настройках проекта должна быть привязка к репозиторию. Иначе пуш ничего не собирает, а выглядит как «деплой долго идёт».
4. Дальше правки только через push, не через ручной деплой из локальной папки: локальная копия бывает неполной, и картинки исчезают с сайта.

## Путь C — GitHub Pages

Settings → Pages → Source: `main`, папка `/`. Сайт появится на `https://<user>.github.io/<repo>/`. На project Pages сайт живёт в подпути `/<repo>/`: используй относительные ссылки на изображения и страницы, иначе получишь 404. Красивые маршруты вроде `/privacy` без дополнительной настройки не работают — используй `privacy.html`. Домен — через файл `CNAME`.

## Путь D — Framer / Webflow

Если на Шаге 6 выбран no-code: Council выдаёт структуру секций и тексты, ты собираешь в редакторе и публикуешь кнопкой Publish. Домен подключается в настройках проекта.

## Путь E — свой сервер

nginx или Caddy, статическая папка, HTTPS через Let's Encrypt. Нужен только если есть причина не использовать A–C.

---

## Формы без бэкенда: HTML → Google Apps Script → Google Sheets

1. Создай Google-таблицу, первая строка — названия полей формы.
2. Расширения → Apps Script, вставь:

```javascript
function json(payload) {
  return ContentService.createTextOutput(JSON.stringify(payload))
    .setMimeType(ContentService.MimeType.JSON);
}

function safeCell(value) {
  const text = String(value || '').trim().slice(0, 2000);
  // Не даём пользовательскому вводу превратиться в формулу Google Sheets.
  return /^[=+\-@]/.test(text) ? "'" + text : text;
}

function doPost(e) {
  const params = (e && e.parameter) || {};
  // Поле website должно быть скрытым honeypot в HTML-форме.
  if (params.website) return json({ ok: true });

  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  const allowed = new Set(headers.concat(['website']));
  const unknown = Object.keys(params).filter(key => !allowed.has(key));
  if (unknown.length) return json({ ok: false, error: 'unexpected_fields' });
  if (headers.includes('email') && params.email &&
      !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(params.email))) {
    return json({ ok: false, error: 'invalid_email' });
  }

  const row = headers.map(header =>
    header === 'timestamp' ? new Date() : safeCell(params[header])
  );

  const lock = LockService.getScriptLock();
  lock.waitLock(5000);
  try {
    sheet.appendRow(row);
  } finally {
    lock.releaseLock();
  }
  return json({ ok: true });
}
```

3. Скрипт должен быть привязан именно к этой таблице. Развертывание → Новое развертывание → Веб-приложение → Доступ: «Все». Скопируй URL.
4. Вставь URL в `action` формы и добавь honeypot, скрытый стилями, а не только названием поля:

```html
<div class="form-trap" aria-hidden="true">
  <label>Не заполняйте это поле <input name="website" tabindex="-1" autocomplete="off"></label>
</div>
<style>
  .form-trap { position: absolute; left: -10000px; width: 1px; height: 1px; overflow: hidden; }
</style>
```

Если используешь `fetch`, сначала проверь CORS и редирект Apps Script в реальном браузере: не показывай успех до подтверждённого ответа.
5. Правила: endpoint не меняется при правках формы; старые поля остаются под теми же именами; добавил поле — добавь колонку в таблицу.
6. **Проверь живой отправкой**, что заявка дошла. Ошибку отправки показывать пользователю, а не глотать: молчащая форма теряет заявки месяцами.

Этот минимальный пример подходит только для учебного или малотрафикового проекта без чувствительных данных. Публичный endpoint можно заспамить. До реального запуска добавь honeypot, allowlist имён полей, ограничения длины и мониторинг; для заметного трафика используй form backend с rate limiting и CAPTCHA/Turnstile. Рядом с формой объясни цель сбора данных и дай ссылку на Privacy Policy. Не собирай этим примером платежи, здоровье, документы, данные детей или пароли.

---

## Домен и почта

- Домен: Namecheap, Cloudflare или регистратор региона. DNS: `A`/`CNAME` по инструкции хостинга.
- Почта на домене: Google Workspace или Zoho. Для отправки писем с сайта — Resend или Brevo, обязательно SPF и DKIM.

---

## После запуска — проверить в живом браузере

- [ ] Открыть сайт на телефоне и на десктопе, прокрутить до конца: нет «дыр» от несработавших анимаций
- [ ] Консоль браузера без ошибок, вкладка Network без 404 на картинки и шрифты
- [ ] Отправить форму — заявка в таблице
- [ ] Событие аналитики на CTA ушло (смотреть тело запроса, а не адрес)
- [ ] PageSpeed прогнан для Mobile и Desktop
- [ ] Legal-страницы открываются из футера
- [ ] Honeypot/антиспам сработал, лишние поля не записываются
- [ ] В репозитории и истории Git нет секретов или service-account JSON
