from flask import Flask, request, jsonify
import logging
import requests
import uuid

app = Flask(__name__)
app.url_map.strict_slashes = False
slave_idx = 0

slaves = []


@app.route("/")
def main():
    if len(slaves) == 0:
        return "No slave nodes", 503
    global slave_idx
    slave = slaves[slave_idx]
    slave_idx = (slave_idx + 1) % len(slaves)
    r = requests.get(url="http://{}:{}".format(slave[0], slave[1]))
    return r.text


@app.route("/register-slave", methods=["GET"])
def register_slave():
    host = request.args.get("host", "")
    port = request.args.get("port", "")
    logging.info("Register {}:{}".format(host, port))
    global slaves
    if (host, port) not in slaves:
        slaves.append((host, port))
    return "ok"


def all_counter():
    slave = slaves[0]
    r = requests.get(url="http://{}:{}/all-counter".format(slave[0], slave[1]))
    res = r.json()
    return "\n".join(res)


@app.route("/counter", methods=["GET"])
def all_counter_handler():
    return all_counter()


@app.route("/counter", methods=["POST"])
def add_counter():
    if len(slaves) == 0:
        return "No slave nodes", 503
    to = request.args.get("to", None, type=int)
    if to is None:
        # Get all uuid
        return "Argument 'to' is required", 400
    app.logger.info("add_counter to={}".format(to))
    counter_uuid = uuid.uuid4()
    app.logger.info("add_counter uuid={}".format(counter_uuid))
    idx = hash(str(counter_uuid)) % len(slaves)
    slave = slaves[idx]
    app.logger.info("add_counter slave={}:{}".format(slave[0], slave[1]))
    r = requests.get(
        url="http://{}:{}/add-counter".format(slave[0], slave[1]),
        params={"to": to, "uuid": counter_uuid},
    )
    if not r.ok:
        return r.text, r.status_code

    return str(counter_uuid)


@app.route("/counter/<uuid>", methods=["GET"])
def get_counter(uuid):
    if len(slaves) == 0:
        return "No slave nodes", 503
    app.logger.info("get_counter uuid={}".format(uuid))
    idx = hash(uuid) % len(slaves)
    slave = slaves[idx]
    app.logger.info("get_counter slave={}:{}".format(slave[0], slave[1]))
    r = requests.get(
        url="http://{}:{}/get-counter".format(slave[0], slave[1]), params={"uuid": uuid}
    )
    if not r.ok:
        return r.text, r.status_code

    return jsonify(r.json()), r.status_code


@app.route("/counter/<uuid>/stop", methods=["POST"])
def delete_counter(uuid):
    if len(slaves) == 0:
        return "No slave nodes", 503
    app.logger.info("delete_counter uuid={}".format(uuid))
    idx = hash(uuid) % len(slaves)
    slave = slaves[idx]
    app.logger.info("delete_counter slave={}:{}".format(slave[0], slave[1]))
    r = requests.get(
        url="http://{}:{}/delete-counter".format(slave[0], slave[1]), params={"uuid": uuid}
    )
    if not r.ok:
        return r.text, r.status_code

    return r.text, r.status_code
