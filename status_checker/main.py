from flask import Flask, render_template, Response
from flask_restful import Api
from status import Status, Logs
from update_status import UpdateStatus
import platform
import logging
from logging import handlers
from utils import read_config
import json

app = Flask(__name__,
            static_folder="./templates/static",
            template_folder="./templates")
api = Api(app)

api.add_resource(Logs,
                 '/get_logs',
                 '/get_logs/<int:limit>',
                 '/get_logs/<string:target_name>',
                 '/get_logs/<string:target_name>/<int:limit>')
api.add_resource(Status,
                 '/get_status')
api.add_resource(UpdateStatus,
                 '/update_status',
                 '/update_status/',
                 '/update_status/<string:target_name>')


@app.route('/')
def index(name=None):
    return render_template('index.html')


@app.route('/simple')
def index_simple(name=None):
    targets = json.loads(Status().get().get_data(as_text=True))
    all_logs = json.loads(Logs().get().get_data(as_text=True))
    version = python_version().get_data(as_text=True)
    config = read_config()
    return render_template('index_simple.html',
                           targets=targets,
                           all_logs=all_logs,
                           version=version,
                           debug=config.getboolean('debug-mode', False))


@app.route('/python_version')
def python_version():
    version = str(platform.python_version())
    resp = Response(version)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def setup_logging():
    # Max log file size - 5Mb
    max_log_file_size = 1024 * 1024 * 5
    max_log_file_count = 10
    log_file_name = 'logs/logs.log'
    logger = logging.getLogger('logger')
    logger.setLevel(logging.INFO)
    handler = handlers.RotatingFileHandler(log_file_name,
                                           'a',
                                           max_log_file_size,
                                           max_log_file_count)
    formatter = logging.Formatter(fmt='[%(asctime)s][%(filename)s->%(funcName)s:%(lineno)d][%(levelname)s] %(message)s',
                                  datefmt='%d/%b/%Y:%H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def run_flask():
    setup_logging()
    logger = logging.getLogger('logger')
    logger.info('Starting app...')
    config = read_config()
    debug_mode = config.getboolean('debug-mode', False)
    port = config.getint('port', 80)
    app.run(host='0.0.0.0',
            port=port,
            debug=debug_mode,
            threaded=True)


if __name__ == '__main__':
    run_flask()
