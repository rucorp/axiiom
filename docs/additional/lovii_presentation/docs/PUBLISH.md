# LOVII — Публикация лендинга

## Структура проекта

```
lovii_presentation/
├── index.html              # Главная страница (инвестиционный лендинг)
├── lovii.ru.html           # Splash-страница для домена lovii.ru
├── presentation.html       # Страница презентации (PDF слайды)
├── strategy.html           # Стратегический план развития
├── pdf/
│   └── LOVII_Strategy.pdf  # PDF со стратегией
├── img/
│   ├── logos/
│   │   ├── lovii-logo.svg          # Логотип светлый
│   │   └── lovii-logo_dark.svg     # Логотип тёмный
│   ├── screenshots/
│   │   └── *.png            # Скриншоты системы
│   └── pdf_images/
│       └── *.png            # Конвертированные PDF слайды
├── css/
│   ├── theme.css            # CSS переменные (темы)
│   └── main.css             # Основные стили (не используется)
└── docs/
    └── PUBLISH.md           # Этот файл
```

## Публикация на GitHub Pages

### 1. Repository настроен для GitHub Pages
Репозиторий уже настроен — GitHub Pages активирован на ветке `main`.

**URL лендинга:** https://bestdeejay-design.github.io/lovii_presentation/

### 2. Автоматическое развёртывание
Каждый push в ветку `main` автоматически публикует изменения на GitHub Pages.

```bash
git add .
git commit -m "описание изменений"
git push
```

Через ~1-2 минуты изменения появятся на сайте.

---

## Публикация на отдельном домене (lovii.ru)

### Вариант 1: GitHub Pages + CNAME

1. Создайте файл `CNAME` в корне репозитория (без расширения):
```
lovii.ru
```

2. В настройках репозитория (Settings → Pages → Custom domain) добавьте `lovii.ru`

3. Настройте DNS у вашего регистратора:
   - Тип: `CNAME`
   - Host: `www`
   - Value: `bestdeejay-design.github.io`

   Или для апата напрямую (без www):
   - Тип: `A` записи:
     - `185.199.108.153`
     - `185.199.109.153`
     - `185.199.110.153`
     - `185.199.111.153`

4. Файл `lovii.ru.html` будет доступен по адресу `lovii.ru/lovii.ru.html`

5. Для корневого адреса `lovii.ru` → переименуйте файл в `index.html` или настройте редирект.

### Вариант 2: Vercel / Netlify

1. Подключите репозиторий к Vercel или Netlify
2. Деплой произойдёт автоматически
3. Подключите свой домен в настройках

### Вариант 3: Хостинг (beget, timeweb и т.д.)

1. Скачайте все файлы проекта
2. Загрузите на хостинг через FTP/SFTP
3. Настройте домен

---

## Файлы для скачивания

Для ручной публикации скачайте следующие файлы и папки:

```
lovii_presentation/
├── index.html
├── lovii.ru.html
├── presentation.html
├── strategy.html
├── css/
│   ├── theme.css
│   └── main.css
├── img/
│   ├── logos/
│   └── screenshots/
├── pdf/
└── pdf_images/
```

---

## Контакты на сайте

- **Телефон:** +7 (911) 928-74-78
- **Email:** invest@lovii.ru, hello@lovii.ru
- **Сайт:** aoplatforma.ru

---

## Страницы сайта

| Страница | URL | Назначение |
|----------|-----|------------|
| Главная | `/` | Инвестиционный лендинг |
| Splash | `/lovii.ru.html` | Страница для домена lovii.ru |
| Презентация | `/presentation.html` | PDF слайды для инвесторов |
| Стратегия | `/strategy.html` | Стратегический план |

---

## Обновление контента

### Редактирование текста
Откройте нужный `.html` файл и измените текст между тегами `<p>`, `<h1>`, `<h2>` и т.д.

### Изменение цветовой схемы
В файле `css/theme.css` измените переменные `--accent-color` и другие.

### Добавление изображений
1. Положите файл в папку `img/`
2. Добавьте `<img src="img/filename.png">` в HTML

### Обновление PDF
Замените файл `pdf/LOVII_Strategy.pdf` — страница `strategy.html` ссылается на него.