# Простой A/B-тест блока с GA4

Этот рецепт подходит для небольшого клиентского эксперимента, а не для сложной платформы экспериментов.

## Назначение варианта

Запускай назначение только после того, как твой consent manager разрешил нужное хранилище и аналитику. До этого показывай обычную контрольную версию без записи в браузерное хранилище:

```html
<script>
  function startHeroExperiment() {
    const experiment = 'hero_v1';
    const storageKey = `experiment:${experiment}`;
    let variant = null;

    try {
      variant = localStorage.getItem(storageKey);
      if (!['A', 'B'].includes(variant)) {
        variant = crypto.getRandomValues(new Uint32Array(1))[0] % 2 ? 'A' : 'B';
        localStorage.setItem(storageKey, variant);
      }
    } catch (error) {
      variant = crypto.getRandomValues(new Uint32Array(1))[0] % 2 ? 'A' : 'B';
    }

    document.documentElement.dataset.heroVariant = variant;
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: 'experiment_view', experiment, variant });
  }

  // Вызови startHeroExperiment() из callback своего consent manager.
</script>
```

Обе версии должны существовать в DOM или коде, но показывается только назначенная. При отправке формы или основном CTA передавай те же `experiment` и `variant` вместе с conversion event.

## Ограничения

- Не делай вывод по нескольким заявкам. До старта зафиксируй primary metric, минимальный полезный эффект и срок теста.
- Не меняй одновременно оффер, дизайн и аудиторию: результат невозможно интерпретировать.
- Не отправляй GA4/GTM события до согласия там, где оно требуется.
- `localStorage`-назначение не связывает устройства и может очищаться пользователем. Для серьёзного теста нужен серверный assignment и отдельная статистическая методика.
- Заранее зафиксируй варианты, аудиторию, primary metric и дату остановки. После запуска не меняй вариант посередине теста.
- Проверь, что `experiment` и `variant` доступны в отчётах GA4; при необходимости зарегистрируй их как custom dimensions.
- Исключи внутренний и тестовый трафик и проверь явный перекос распределения A/B до анализа результата.
