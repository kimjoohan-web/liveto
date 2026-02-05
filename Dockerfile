FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "myproject.asgi:application"]