FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP master.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 5999
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./master/* /code/
CMD ["flask", "run"]