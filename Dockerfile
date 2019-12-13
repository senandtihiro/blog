FROM python:3.7.1

WORKDIR /server

ADD . /server

RUN pip install --upgrade pip

RUN pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

EXPOSE 8000

CMD gunicorn app:app --bind 0.0.0.0:8000 --worker-class sanic.worker.GunicornWorker
