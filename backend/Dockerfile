FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /var/www/html/backend
WORKDIR /var/www/html/backend
ADD . /var/www/html/backend

RUN pip install uwsgi pipenv==2022.6.7 -i https://pypi.douban.com/simple/ && \
  pipenv lock -r > requirements.txt && \
  pip install -r requirements.txt
RUN sed -i 's/\r//' ./start.sh
RUN chmod +x ./start.sh
