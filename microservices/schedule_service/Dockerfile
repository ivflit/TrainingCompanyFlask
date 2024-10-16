FROM python:3.11
 
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5006
CMD ["python", "app.py"]
