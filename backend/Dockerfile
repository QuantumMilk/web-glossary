# Используем официальный образ Python
FROM python:3.9-slim

# Создадим рабочую директорию
WORKDIR /app

# Скопируем файл зависимостей
COPY requirements.txt .

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем код бэкенда
COPY . /app

# Откроем порт 8080
EXPOSE 8080

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
