FROM python:3.11-bullseye

ENV PYTHONBUFFERED=1

WORKDIR /LMS

COPY requirements.txt ./

RUN apt-get update && apt-get install -y libgl1-mesa-glx \
    && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000