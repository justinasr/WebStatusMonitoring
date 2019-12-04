from flask import Flask, render_template
from flask_restful import Api
from status import Status, Logs
from update_status import UpdateStatus
from utils import read_config, setup_file_logging
import json
import logging


app = Flask(__name__,
            static_folder="./templates/static",
            template_folder="./templates")
api = Api(app)


api.add_resource(Logs,
                 '/get_logs',
                 '/get_logs/<int:limit>',
                 '/get_logs/<string:target_id>',
                 '/get_logs/<string:target_id>/<int:limit>')
api.add_resource(Status,
                 '/get_status')
api.add_resource(UpdateStatus,
                 '/update_status',
                 '/update_status/',
                 '/update_status/<string:target_id>')


@app.route('/')
def index(name=None):
    return render_template('index.html')


@app.route('/simple/')
def index_simple(name=None):
    targets = json.loads(Status().get().get_data(as_text=True))
    all_logs = json.loads(Logs().get().get_data(as_text=True))
    config = read_config()
    return render_template('index_simple.html',
                           targets=targets,
                           all_logs=all_logs,
                           debug=bool(int(config.get('debug-mode', 0))))


def run_flask():
    setup_file_logging()
    logger = logging.getLogger('logger')
    logger.info('Starting app...')
    config = read_config()
    host = config.get('host')
    debug_mode = bool(int(config.get('debug-mode', 0)))
    port = int(config.get('port'))
    app.run(host=host,
            port=port,
            debug=debug_mode,
            threaded=True)


if __name__ == '__main__':
    run_flask()
