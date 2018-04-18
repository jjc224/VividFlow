from flask import Flask, request, url_for, session, redirect
from flask.sessions import SessionInterface

app = Flask(__name__)

import dbconn
import json
import Constants
from Algorithm import Algorithm
from Module import ModuleNode
import JobScheduler
import User

# The secret likes to be here
app.secret_key = '(w*32987ER(p&*eh23BNU()]'

execfile("routes/routes.py")

if __name__ == '__main__':
    scheduler = JobScheduler.StartJobSchedulerAsThread()
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
