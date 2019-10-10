from flask import Flask, request, jsonify
import requests
import socket
import logging
import time

logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)


class Counter:
    def __init__(self, to, uuid):
        self.start = int(time.time())
        self.to = to
        self.uuid = uuid

    def get_current(self):
        curr = int(time.time())
        return curr - self.start


class Counters:
    def __init__(self):
        self.counters = []

    def add_counter(self, cnt):
        if not isinstance(cnt, Counter):
            raise RuntimeError("Counter must be the instance of class Counter")
        self.counters.append(cnt)

    def get_counter(self, uuid):
        for cnt in self.counters:
            if uuid == cnt.uuid:
                return cnt
        return None

    def delete_counter(self, uuid):
        for cnt in self.counters:
            if uuid == cnt.uuid:
                self.counters.remove(cnt)
                return


counters = Counters()


@app.route("/")
def main():
    return "{}\n".format(socket.getfqdn())


@app.route("/add-counter", methods=["GET"])
def add_counter():
    to = request.args.get("to", None, type=int)
    uuid = request.args.get("uuid", None, type=str)
    global counters
    counters.add_counter(Counter(to, uuid))
    return ""


@app.route("/get-counter", methods=["GET"])
def get_counter():
    uuid = request.args.get("uuid", None, type=str)
    global counters
    cnt = counters.get_counter(uuid)
    if cnt is None:
        return "Counter {} is not found on {}".format(uuid, socket.getfqdn()), 404

    return jsonify({"current": cnt.get_current(), "to": cnt.to})


def register_to_master():
    # Register to master
    master_host = "cnt_master"
    master_port = 5999
    url = "http://{}:{}/register-slave".format(master_host, master_port)
    self_hostname = socket.getfqdn()
    app.logger.info("Register self: {}:{} to {}".format(self_hostname, 6000, url))
    r = requests.get(url=url, params={"host": self_hostname, "port": 6000})
    if not r.ok:
        app.logger.error(
            "Failed to register. Return {}. Body:\n{}".format(r.status_code, r.text)
        )


register_to_master()
