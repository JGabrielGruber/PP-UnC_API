FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

WORKDIR /usr/src/app/src

CMD [ "gunicorn", "-b", "0.0.0.0:8000", "--log-level LEVEL", "app:__hug_wsgi__" ]
