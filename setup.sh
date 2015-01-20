#!/bin/bash
# #!/usr/bin/env python3

python3 -m venv --without-pip flask
source flask/bin/activate
curl https://bootstrap.pypa.io/get-pip.py | python3
deactivate
source flask/bin/activate

pip3 install flask flask-login flask-openid flask-mail flask-sqlalchemy sqlalchemy-migrate flask-whooshalchemy flask-wtf flask-babel guess_language flipflop coverage

