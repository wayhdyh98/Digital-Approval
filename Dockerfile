FROM python:3.8-slim

#RUN apt-get clean && apt-get -y update

EXPOSE 5000

COPY ./ /app

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r /app/requirements.txt --src /usr/local/src

WORKDIR /app

CMD [ "gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "server:app" ]