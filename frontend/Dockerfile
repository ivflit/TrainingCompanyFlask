FROM python:3.11
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8007
CMD ["python", "app.py"]
