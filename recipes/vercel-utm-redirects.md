# Короткие UTM-ссылки в Vercel

Короткая ссылка `/tg` удобна человеку, а аналитика получает размеченный переход. Добавь `vercel.json` в корень сайта:

```json
{
  "redirects": [
    {
      "source": "/tg",
      "destination": "/?utm_source=telegram&utm_medium=community&utm_campaign=webinar",
      "permanent": false
    }
  ]
}
```

Правила:

- Используй временный redirect, пока проверяешь разметку.
- UTM ставятся только на входящий внешний переход. Не добавляй их к внутренним ссылкам сайта: это портит атрибуцию сессии.
- Названия `source`, `medium`, `campaign` зафиксируй в таблице аналитики до публикации.
- После деплоя открой `/tg`, проверь конечный URL и появление source/medium в DebugView или realtime-отчёте GA4.
