FROM alpine:3.8

RUN apk add --no-cache python3 py-pip ca-certificates \
  && pip install virtualenv

WORKDIR /app

COPY . /app
RUN virtualenv -p python3 /venv && /venv/bin/pip install -r requirements.txt

EXPOSE 8080
ENV PYTHONUNBUFFERED=1
CMD ["/venv/bin/gunicorn", "--config", "/app/gunicorn.conf", "--log-config", "/app/logging.conf", "-b", ":3000", "wsgi"]