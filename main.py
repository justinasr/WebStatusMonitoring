from flask import Flask, render_template
from flask_restful import Api
from status import Status, Logs
from update_status import UpdateStatus
import platform
import logging
from logging import handlers

app = Flask(__name__)
api = Api(app)

api.add_resource(Logs, '/get_logs', '/get_logs/<int:limit>', '/get_logs/<string:target_name>', '/get_logs/<string:target_name>/<int:limit>')
api.add_resource(Status, '/get_status')
api.add_resource(UpdateStatus, '/update_status', '/update_status/', '/update_status/<string:target_name>')


@app.route('/')
def index(name=None):
    targets = Status().get()
    all_logs = Logs().get()
    version = str(platform.python_version())
    return render_template('index.html', targets=targets, all_logs=all_logs, version=version)


def setup_logging():
    # Max log file size - 5Mb
    max_log_file_size = 1024 * 1024 * 5
    max_log_file_count = 10
    log_file_name = 'logs/logs.log'
    logger = logging.getLogger('logger')
    logger.setLevel(logging.INFO)
    handler = handlers.RotatingFileHandler(log_file_name, 'a', max_log_file_size, max_log_file_count)
    formatter = logging.Formatter(fmt='[%(asctime)s][%(filename)s->%(funcName)s:%(lineno)d][%(levelname)s] %(message)s', datefmt='%d/%b/%Y:%H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def run_flask():
    setup_logging()
    logger = logging.getLogger('logger')
    logger.info('Starting app...')
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    run_flask()
