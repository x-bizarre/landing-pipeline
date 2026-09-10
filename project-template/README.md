# project-template — папка одного лендинга

Скопируй эту папку под каждый новый лендинг (`cp -r project-template ../my-landing`). Все артефакты шагов сохраняются сюда, статус ведётся в `STATUS.md`. Это заменяет внешний трекер: любой LLM, открыв `STATUS.md`, видит, на каком шаге проект, какие решения приняты и где лежат файлы.

```
my-landing/
├── STATUS.md                 ← статус шагов, решения, ссылки на артефакты
├── 01-discovery/discovery-brief.md
├── 02-reviews/reviews-synthesis.md
├── 03-custdev/custdev-synthesis.md  (+ custdev-transcript-NN.md по запросу)
├── 04-copy/copy-brief.md
├── 05-design/hero-v1.html … design-tokens.json, component-library.md
├── 06-landing/landing.html, privacy.html, terms.html, cookies.html, images/
├── 07-polish/seo-patches.md, mobile-patches.md, pagespeed-analysis.md
└── launch-checklist.md
```

Как продолжить работу в новой сессии: «Открой `STATUS.md`, прочитай, на каком мы шаге, подними артефакты предыдущих шагов по ссылкам и продолжай со следующего».
