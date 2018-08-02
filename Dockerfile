FROM python:alpine3.6
RUN python --version

COPY . /sample-app
WORKDIR /sample-app

RUN apk add --update --no-cache --virtual build-deps gcc python3-dev musl-dev libc-dev linux-headers libxslt-dev libxml2-dev \
&& apk add libffi-dev openssl-dev \
&& pip install --upgrade pip setuptools \
&& pip install -r requirements.txt \
&& apk del build-deps

CMD [ "python", "runner.py" ]