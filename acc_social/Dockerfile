FROM python:3.11

WORKDIR /social-acc

COPY requirements.txt /social-acc/

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
