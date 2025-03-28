## XML Parser API

### Описание

Flask-приложение для обработки XML-файлов. При загрузке XML:

- сохраняет имя файла;
- сохраняет все теги и их атрибуты в базу данных;
- реализует простой API для получения информации о тегах и их атрибутах.

Используется парсинг через `xml.sax` и база данных SQLite.

---

### Возможности

- Загрузка XML-файлов и парсинг их содержимого `/api/file/read`
- Получение количества тегов по имени в конкретном файле `/api/tags/get-count`
- Получение уникальных атрибутов заданного тега в
  файле `/api/tags/attributes/get`

---

### Как запустить в Docker

1. Клонируйте репозиторий:

```bash
git clone https://github.com/faiver-90/test_work_4417995056.git .
```

2. Постройте и запустите контейнер:

```bash
docker-compose up --build -d
```

3. Приложение будет доступно по адресу:

```
http://localhost:5000
```

---

### Примеры запросов

**Проверка работы**

```bash
curl "http://localhost:5000/test"
```

**Загрузка XML-файла:**

```bash
curl -X POST http://localhost:5000/api/file/read \
  -F "file=@example.xml"
```

**Получение количества тегов:**

```bash
curl "http://localhost:5000/api/tags/get-count?file=example.xml&tag=person"
```

**Получение атрибутов тега:**

```bash
curl "http://localhost:5000/api/tags/attributes/get?file=example.xml&tag=person"
```

---

### Требования

- Docker и Docker Compose
- Python 3.10+ (если запускать без Docker)

---
