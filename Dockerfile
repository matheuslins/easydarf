FROM python:3.9.1-alpine

WORKDIR /app

COPY . /app
ADD . .

EXPOSE 8080

RUN pip3 install -r requirements.txt

CMD [ "python", "/app/main.py" ]