# Python bazaviy imidj
FROM python:3.10

# Ishchi papkani yaratish
WORKDIR /app

# Fayllarni konteynerga ko‘chirish
COPY . .

# Kutubxonalarni o‘rnatish
RUN pip install --no-cache-dir -r requirements.txt

# Botni ishga tushurish
CMD ["python", "Bot.py"]
