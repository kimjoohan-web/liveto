FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/
# RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /app/
# Channels 실행을 위해 daphne 사용 권장
CMD ["daphne", "-b", "0.0.0.0", "-p", "80", "config.asgi:application"]