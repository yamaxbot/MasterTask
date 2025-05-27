# Используем официальный образ Python
FROM python:3.10

WORKDIR /app

COPY requirements.txt reaquirements.txt

# Устанавливаем зависимости
RUN pip install -r reaquirements.txt

# Запускаем бота
CMD ["python", "main.py"]