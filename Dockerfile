FROM python

ADD . /app

WORKDIR /app

RUN apt-get install wkhtmltopdf -y
RUN pip install -r requirements.txt

CMD ["python", "telegram_update.py"]
