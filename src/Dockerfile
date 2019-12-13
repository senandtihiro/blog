FROM python:3.7.1

WORKDIR /server

ADD . /temp1

RUN pip install --upgrade pip

RUN pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

EXPOSE 8000

CMD gunicorn run:app --bind 0.0.0.0:8000 --worker-class sanic.worker.GunicornWorker
