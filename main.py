from flask import Flask
from flask_restful import Api
from status import Status
from update_status import UpdateStatus

app = Flask(__name__)
api = Api(app)

api.add_resource(Status, '/')
api.add_resource(UpdateStatus, '/update_status', '/update_status/<string:target_name>')


def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    run_flask()
