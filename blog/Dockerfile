FROM debian

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip && \
    pip3 install flask flask-sqlalchemy

CMD ["python3", "app.py"]
