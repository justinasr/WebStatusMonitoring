from flask import Flask, render_template
from flask_restful import Api
from status import Status, Logs
from update_status import UpdateStatus
import platform

app = Flask(__name__)
api = Api(app)

api.add_resource(Logs, '/get_logs', '/get_logs/<int:limit>', '/get_logs/<string:target_name>', '/get_logs/<string:target_name>/<int:limit>')
api.add_resource(Status, '/get_status')
api.add_resource(UpdateStatus, '/update_status', '/update_status/<string:target_name>')


@app.route('/')
def index(name=None):
    targets = Status().get()
    all_logs = Logs().get()
    version = str(platform.python_version())
    return render_template('index.html', targets=targets, all_logs=all_logs, version=version)


def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    run_flask()
