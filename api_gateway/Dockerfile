FROM python:3.10-slim
# Tells python not to generate .pyc
ENV PYTHONDONTWRITEBYTECODE=1 
# Tells Python to run in unbuffered mode - makes output appear immediately
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
