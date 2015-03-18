#!/usr/bin/env python3
from app import app
# app.run(debug=True, host='0.0.0.0')

import eventlet
from eventlet import wsgi
wsgi.server(eventlet.listen(('', 5000), backlog=500), app, max_size=8000)
