#!/usr/bin/env python3
from app import app
app.run(debug=True, host='0.0.0.0', threaded=True)
# (threaded=True, processes=3)
