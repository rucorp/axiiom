![AXIIOM](assets/header.svg)

# AXIIOM

Разработка в сфере финтеха: сайты, мобильные приложения, UI/UX-дизайн.

**🌐 Версии:** [English](README.md) · [Русский](README.ru.md) · [Сайт](https://axiiom.ru)

[![Static Site](https://img.shields.io/badge/site-static%20HTML%2FCSS%2FJS-blue)](https://axiiom.ru)
[![Accessibility](https://img.shields.io/badge/Lighthouse%20a11y-100-brightgreen)](https://axiiom.ru)
[![SEO](https://img.shields.io/badge/Lighthouse%20SEO-100-brightgreen)](https://axiiom.ru)
[![Pages Checked](https://img.shields.io/badge/test_site-79%20pages%20%2F%203476%20checks-brightgreen)](https://axiiom.ru)
[![License](https://img.shields.io/badge/license-proprietary-lightgrey)](https://axiiom.ru)
[![Deploy](https://img.shields.io/badge/deploy-nginx%3Aalpine-blue)](https://axiiom.ru)

## Статус

| Проверка | Результат |
|---|---|
| страниц в `test_site.py` | 79 |
| проверок в `test_site.py` | 3476 |
| неудачных в `test_site.py` | 0 |
| счётчик прогонов `test_site.py` | 3232 пройдено / 244 предупреждения |
| Lighthouse доступность | 100 |
| Lighthouse SEO | 100 |

## О компании

AXIIOM (ООО «Аксиома») — российская компания по разработке в сфере финтеха, основанная в 2004 году, с офисами в Санкт-Петербурге и Москве. Компания создаёт финтех-решения: платёжные системы, платформы лояльности и кредитные конвейеры. Услуги включают сайты, мобильные приложения и UI/UX-дизайн. Контент сайта ведётся на русском языке.

Этот репозиторий — исходный код публичного сайта [https://axiiom.ru](https://axiiom.ru). Это полностью статический сайт без серверного фреймворка.

## Быстрый старт

Запустите локальную копию любым статическим сервером:

```bash
python3 -m http.server 8000
# затем откройте http://localhost:8000
```

Или соберите продакшн-сборку и отдайте через nginx в Docker:

```bash
python3 build.py
docker build -t axiiom .
docker run -p 8080:80 axiiom
```

## Сборка

`build.py` минифицирует исходные ассеты через esbuild и формирует готовый к деплою результат:

```bash
python3 build.py
```

## Структура репозитория

```
axiiom/
├── build.py                 # минификация через esbuild + сборка
├── nav.src.js               # исходник навигации (рендерит nav.js)
├── styles.src.css           # исходник стилей (CSS-токены в DESIGN.md)
├── DESIGN.md                # дизайн-система, CSS-токены, тёмная/светлая тема
├── test_site.py             # проверка сайта (79 страниц, 3476 проверок)
├── config.js                # конфигурация сайта
├── theme.js                 # переключение тёмной/светлой темы
├── preloader.js             # прелоадер страницы
├── metrika.js               # интеграция Яндекс.Метрики
├── footer.js                # рендеринг подвала
├── index.html               # главная страница
├── 404.html                 # страница ошибки
├── industries/              # 23 отраслевые страницы
├── blog/                    # 7 записей в блоге
├── tools/                   # 12 инструментов
├── calculator/              # страница калькулятора
├── demo/app/                # 16 демо-страниц
├── docs/                    # документация
├── privacy/                 # политика конфиденциальности
├── terms/                   # условия использования
├── robots.txt
├── sitemap.xml              # 79 URL
├── Dockerfile               # образ деплоя nginx:alpine
├── Makefile
├── CNAME                    # axiiom.ru
└── assets/                  # сгенерированный SVG (header.svg, footer.svg)
```

## Стек

- **Чистый HTML/CSS/JS** без фронтенд-фреймворка.
- **esbuild** для минификации под управлением `build.py`.
- **nginx:alpine** — Docker-образ для деплоя.
- **Яндекс.Метрика** и **Google Analytics** для аналитики (`metrika.js`).
- **CSS-токены** для тёмной/светлой темы, описаны в `DESIGN.md`.
- Навигация рендерится через `nav.js` из исходника `nav.src.js`.

## Деплой

Сайт опубликован по адресу [https://axiiom.ru](https://axiiom.ru) (указан в `CNAME`). В разделе About репозитория укажите тот же URL как домашнюю страницу GitHub Pages.

## Ключевые слова

финтех, статический сайт, дизайн-система, доступность, UI/UX, платёжные системы, платформы лояльности, кредитные конвейеры.

![AXIIOM](assets/footer.svg)
