FROM python

ADD . /app

RUN apt update \
	&& apt-get install wkhtmltopdf xvfb -y

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "telegram_update.py"]
