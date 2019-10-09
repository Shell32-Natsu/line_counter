from flask import Flask, request
import logging

app = Flask(__name__)

slaves = []

@app.route("/")
def hello():
    return str(slaves)

@app.route("/register-slave" ,methods=["GET"])
def register_slave():
    host = request.args.get("host", "")
    port = request.args.get("port", "")
    logging.info("Register {}:{}".format(host, port))
    global slaves
    if (host, port) not in slaves:
        slaves.append((host, port))
    return "ok"