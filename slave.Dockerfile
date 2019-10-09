FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP slave.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 6000
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./slave/* /code/
CMD ["flask", "run"]