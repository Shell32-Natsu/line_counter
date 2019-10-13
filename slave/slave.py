from flask import Flask, request, jsonify
import requests
import socket
import logging
import time
import json
import os

logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)

data_path = "/data"


class Counter:
    def __init__(self, to, uuid):
        self.start = int(time.time())
        self.to = to
        self.uuid = uuid
        self.data_path = data_path

    def get_current(self):
        curr = int(time.time())
        return curr - self.start

    def dump(self):
        content = json.dumps({"uuid": self.uuid, "to": self.to, "start": self.start}, indent=2)
        path = os.path.join(self.data_path, self.uuid)
        if os.path.exists(path):
            raise RuntimeError("Counter {} has already existed".format(self.uuid))
        with open(path, "w") as f:
            f.write(content)

    def load(self):
        path = os.path.join(self.data_path, self.uuid)
        if not os.path.exists(path):
            raise RuntimeError("Counter {} doesn't exist".format(self.uuid))
        content = {}
        with open(path, "r") as f:
            content = json.loads(f.read())
        self.to = content["to"]
        self.uuid = content["uuid"]
        self.start = content["start"]

    def delete(self):
        path = os.path.join(self.data_path, self.uuid)
        if not os.path.exists(path):
            raise RuntimeError("Counter {} doesn't exist".format(self.uuid))
        os.remove(path)

    @staticmethod
    def s_load(uuid):
        cnt = Counter(None, uuid)
        try:
            cnt.load()
        except RuntimeError as e:
            return None
        return cnt

    @staticmethod
    def s_delete(uuid):
        cnt = Counter(None, uuid)
        cnt.delete()

    @staticmethod
    def s_all():
        uuids = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f))]
        res = []
        to_delete = []
        for uuid in uuids:
            cnt = Counter(None, uuid)
            cnt.load()
            if cnt.get_current() >= cnt.to:
                to_delete.append(cnt)
            else:
                res.append(cnt.uuid)

        for cnt in to_delete:
            cnt.delete()

        return res


class Counters:
    def __init__(self):
        pass

    def add_counter(self, cnt):
        if not isinstance(cnt, Counter):
            raise RuntimeError("Counter must be the instance of class Counter")
        cnt.dump()

    def get_counter(self, uuid):
        return Counter.s_load(uuid)

    def delete_counter(self, uuid):
        Counter.s_delete(uuid)

    def all_counters_uuid(self):
        return Counter.s_all()


counters = Counters()


@app.route("/")
def main():
    return "{}\n".format(socket.getfqdn())


@app.route("/add-counter", methods=["GET"])
def add_counter():
    to = request.args.get("to", None, type=int)
    uuid = request.args.get("uuid", None, type=str)
    counters.add_counter(Counter(to, uuid))
    return ""


@app.route("/get-counter", methods=["GET"])
def get_counter():
    uuid = request.args.get("uuid", None, type=str)
    cnt = counters.get_counter(uuid)
    if cnt is None:
        return "Counter {} is not found on {}".format(uuid, socket.getfqdn()), 404
    if cnt.get_current() >= cnt.to:
        counters.delete_counter(uuid)
        return "Counter {} is not found on {}".format(uuid, socket.getfqdn()), 404

    return jsonify({"current": cnt.get_current(), "to": cnt.to})


@app.route("/all-counter", methods=["GET"])
def all_counter():
    return jsonify(counters.all_counters_uuid())


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
