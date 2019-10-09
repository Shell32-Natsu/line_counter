from flask import Flask
import requests
import socket
import logging
logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Slave"

def register_to_master():
    # Register to master
    master_host = "cnt_master"
    master_port = 5999
    url = "http://{}:{}/register-slave".format(master_host, master_port)
    self_hostname = socket.getfqdn()
    app.logger.info("Register self: {}:{} to {}".format(self_hostname, 6000, url))
    r = requests.get(
        url=url,
        params={
            "host": self_hostname,
            "port": 6000
        }
    )
    if not r.ok:
        app.logger.error("Failed to register. Return {}. Body:\n{}".format(r.status_code, r.text))

register_to_master()