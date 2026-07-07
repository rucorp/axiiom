# 🚀 Деплой на GitHub Pages

## ✅ Проект готов к публикации!

Все файлы закоммичены и готовы к пушу на GitHub.

---

## 📋 Инструкция по шагам

### 1. Создайте репозиторий на GitHub

```bash
# Зайдите на https://github.com/new
# Создайте новый пустой репозиторий
# Название: например, pizzanapoli или pizza-napoli-site
```

### 2. Добавьте удаленный репозиторий

**Вариант A: HTTPS (рекомендуется)**
```bash
git remote add origin https://github.com/ВАШ_НИК/pizzanapoli.git
```

**Вариант B: SSH**
```bash
git remote add origin git@github.com:ВАШ_НИК/pizzanapoli.git
```

### 3. Запушьте проект

**Автоматически:**
```bash
./deploy.sh
```

**Или вручную:**
```bash
git push -u origin main
```

### 4. Включите GitHub Pages

1. Зайдите в ваш репозиторий на GitHub
2. Перейдите в **Settings** → **Pages**
3. В разделе **Source** выберите:
   - **Deploy from branch**
4. Выберите ветку и папку:
   - **Branch:** `main`
   - **Folder:** `/ (root)`
5. Нажмите **Save**

### 5. Готово!

Через 1-2 минуты сайт будет доступен по адресу:
```
https://ВАШ_НИК.github.io/pizzanapoli/
```

---

## 🎯 Что будет опубликовано

### Основной сайт (для заказчика):
- **Путь:** `/src/index.html`
- **Контент:** Реальный с pizzanapolirsc.ru
- **Дизайн:** На основе оригинала
- **Будет доступен:** `https://ВАШ_НИК.github.io/pizzanapoli/`

### Premium Concept (альтернатива):
- **Путь:** `/premium-concept/index.html`
- **Дизайн:** Премиум Michelin уровня
- **Будет доступен:** `https://ВАШ_НИК.github.io/pizzanapoli/premium-concept/`

---

## 📁 Структура на GitHub Pages

```
https://ВАШ_НИК.github.io/pizzanapoli/
│
├── index.html              ← Сайт заказчика (ОСНОВНОЙ)
├── premium-concept/
│   └── index.html          ← Premium версия (альтернатива)
├── styles/
├── scripts/
└── Документация (.md файлы)
```

---

## 🔧 Если что-то пошло не так

### Ошибка: "remote origin already exists"
```bash
# Удалите старый remote и добавьте новый
git remote remove origin
git remote add origin https://github.com/ВАШ_НИК/pizzanapoli.git
```

### Ошибка: "Authentication failed"
- Проверьте логин/пароль от GitHub
- Или используйте SSH вместо HTTPS

### Сайт не обновляется на GitHub Pages
```bash
# Принудительный пуш
git push -f origin main

# Или сделайте небольшой изменения и запушьте снова
echo "# Update" >> README.md
git add .
git commit -m "Force update"
git push origin main
```

### Страница не загружается
1. Проверьте, что файл называется `index.html`
2. Убедитесь, что выбран правильный branch (main)
3. Подождите 2-3 минуты (GitHub Pages обновляется не сразу)
4. Проверьте вкладку Actions на GitHub - там должен быть успешный deploy

---

## 💡 Советы

### Для быстрой проверки:
```bash
# Локально проверьте сайт перед пушем
./start.sh
# Откройте http://localhost:8000
```

### После пуша:
1. Откройте сайт на GitHub Pages
2. Проверьте все ссылки
3. Убедитесь, что изображения загружаются
4. Протестируйте форму заказа

### Для обновления:
```bash
# Внесите изменения
git add .
git commit -m "Описание изменений"
git push origin main
# GitHub Pages автоматически обновится через 1-2 минуты
```

---

## 🌐 Прямые ссылки

После деплоя сайт будет доступен:

**Основной сайт:**
```
https://ВАШ_НИК.github.io/pizzanapoli/
```

**Premium концепт:**
```
https://ВАШ_НИК.github.io/pizzanapoli/premium-concept/
```

---

## 📞 Если нужна помощь

1. Проверьте [официальную документацию GitHub Pages](https://docs.github.com/en/pages)
2. Убедитесь, что репозиторий публичный (или включите Pages для приватного)
3. Проверьте лимиты GitHub Pages (100GB трафика в месяц бесплатно)

---

## ✅ Чеклист готовности

- [x] Все файлы закоммичены
- [x] Создан deploy скрипт
- [x] Документация готова
- [ ] Добавлен remote origin
- [ ] Выполнен `git push`
- [ ] Включены GitHub Pages в настройках
- [ ] Сайт доступен по URL

---

**Удачи с деплоем! 🚀**

*Сайт готов к показу заказчику!*
