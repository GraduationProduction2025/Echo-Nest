FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
# mysql日本語環境の追加
COPY my.cnf /etc/mysql/conf.d/my.cnf
RUN apt-get update \
    && apt-get install -y python3-dev default-libmysqlclient-dev build-essential locales \
    && sed -i -e 's/# \(ja_JP.UTF-8\)/\1/' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=ja_JP.UTF-8
ENV LC_ALL ja_JP.UTF-8
ENV TZ Asia/Tokyo
ENV LANG=ja_JP.UTF-8
RUN pip install -r requirements.txt
COPY . /code/
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]