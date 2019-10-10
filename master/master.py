from flask import Flask, request
import logging
import requests

app = Flask(__name__)
slave_idx = 0

slaves = []

@app.route("/")
def main():
    if len(slaves) == 0:
        return "No slave nodes", 503
    global slave_idx
    slave = slaves[slave_idx]
    slave_idx = (slave_idx + 1) % len(slaves)
    r = requests.get(
        url="http://{}:{}".format(slave[0], slave[1])
    )
    return r.text
    

@app.route("/register-slave" ,methods=["GET"])
def register_slave():
    host = request.args.get("host", "")
    port = request.args.get("port", "")
    logging.info("Register {}:{}".format(host, port))
    global slaves
    if (host, port) not in slaves:
        slaves.append((host, port))
    return "ok"