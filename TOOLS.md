# TOOLS — внешние скиллы и сервисы, которые использует пайплайн

Всё, что здесь перечислено, в репозиторий не входит: это чужие проекты со своими лицензиями или онлайн-сервисы. Пайплайн работает и без них, но с ними шаги 0, 5 и 7 получаются точнее.

## Скиллы для Claude Code (и совместимых агентов)

| Скилл | Где брать | На каком шаге | Зачем |
|---|---|---|---|
| **UI/UX Pro Max** | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | 5, 6 | База: 88 стилей, 192 палитр, 74 пар шрифтов, 34 landing patterns, 119 UX-правил, 13 стеков. Копии её CSV-файлов лежат в `05-design/data/` (MIT, с атрибуцией), поэтому шаг 5 работает и в чате, и в Claude Code без установки скилла. Полный скилл даёт ещё 13 стеков и скрипт поиска. Файл `05-design/reference-library.md` можно положить в его `data/` |
| **Marketing skills** | https://github.com/coreyhaines31/marketingskills | 4, 7a | `copywriting`, `page-cro`, `form-cro`, `ai-seo`, `schema-markup`, `seo-audit`, `analytics-tracking`. Полезны как второй проход по Copy Brief и по SEO-слою |
| **Next Move Theory (AJTBD)** | https://github.com/zamesin/Next-Move-Theory-Canon-and-Skills | 0 | `nmt-market-research` даёт вердикт GO / NARROW / PIVOT и сегменты до того, как писать лендинг; `nmt-craft-value-proposition` и `nmt-craft-go-to-market` — ценность и коммуникация под сегмент |
| **GEO-SEO Claude skills** | https://github.com/zubair-trabzada/geo-seo-claude | 7a, после деплоя | Набор скиллов `geo-audit`, `geo-citability`, `geo-crawlers`, `geo-llmstxt`, `geo-schema`, `geo-technical`, `geo-content`, `geo-report`: citability-скоринг, доступ AI-краулеров, `llms.txt`, schema, E-E-A-T, отчёт клиенту. MIT. Важно: балл аудита не равен цитируемости, см. `07-polish/seo-geo-checklist.md` |

Как подключить в Claude Code: положить папку скилла в `~/.claude/skills/<имя>/` с файлом `SKILL.md`. Блоки этого репозитория можно подключить так же: каждый файл `0N-*/…md` — самостоятельная инструкция.

## Онлайн-сервисы

| Сервис | Шаг | Зачем |
|---|---|---|
| Refero Styles — https://styles.refero.design | 5 | Дизайн-системы реальных продуктов как эталон стиля (машиночитаемый DESIGN.md) |
| React Bits — https://www.reactbits.dev | 5, 6 | Бесплатные эффекты в 4 вариантах (JS/TS × CSS/Tailwind) |
| Aceternity UI — https://ui.aceternity.com | 5, 6 | «Вау»-эффекты; часть платная, бесплатных хватает |
| Fancy Components — https://www.fancycomponents.dev | 5, 6 | Редкие эффекты: физика, gooey, stacking cards |
| 21st.dev — https://21st.dev | 6 | Готовые блоки целиком (pricing, hero, footer), есть MCP |
| squoosh.app — https://squoosh.app | 6 | Конвертация картинок в WebP в браузере |
| Lucide / Heroicons / Phosphor | 6 | Иконки вместо эмодзи |
| Google Apps Script + Google Sheets | 6 | Приём форм без бэкенда (`doPost` → таблица) |
| PageSpeed Insights — https://pagespeed.web.dev | 7c | Отчёт по производительности и Core Web Vitals |
| Google Rich Results Test, Schema Markup Validator | 7a | Проверка JSON-LD |
| Vercel / Netlify / GitHub Pages | Финал | Деплой статики |

## Источники отзывов для шага 2

G2, Capterra, Product Hunt (B2B и SaaS) · Reddit (любая ниша) · App Store, Google Play (приложения) · Trustpilot, Amazon (физические товары и e-commerce) · комментарии под видео конкурентов на YouTube. Модель ищет сама, у пользователя детали не спрашивает.
