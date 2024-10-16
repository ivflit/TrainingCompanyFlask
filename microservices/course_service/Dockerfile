FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5004
CMD ["python", "app.py"]
