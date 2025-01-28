# Используем официальный образ Python
FROM python:3.9-slim

# Создадим рабочую директорию
WORKDIR /app

# Скопируем файлы зависимостей
COPY requirements.txt requirements.txt

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем все файлы в контейнер
COPY . .

# Укажем порт, на котором запускается приложение
EXPOSE 8080

# Запуск uvicorn на 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
