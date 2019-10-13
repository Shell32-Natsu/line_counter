# Requirements

This project has been tested in following environment:

```
OS: Fedora 27
Kernel version: 4.18.19
Docker version: 18.09.0, build 4d60db4
Docker compose version: 1.17.1, build 6d101fb
Python runtime: 3.7
```

# How to run

1. Please make sure you have installed docker and docker-compose.
2. Since we need to build image from `python:3.7-alpine` and `jwilder/nginx-proxy` so we need internet connection.
3. Run `bash setup_api.sh [num]` to start server.
4. Run `bash setup_api.sh [num]` when server is running to dynamically change the backend container number.
5. Nginx server will listen on `80` port on `localhost`.
6. Run `bash tear_down.sh` to stop server. **Note that volume `cnt_tmp` will be deleted and all counters will be lost.**

# Tests

There are simple test scripts in the `tests` directory.