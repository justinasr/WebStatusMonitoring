from flask_restful import Resource
from database import Database
from utils import read_config, timestamp_to_string
import json
import logging
import flask


class Status(Resource):

    def __init__(self):
        self.logger = logging.getLogger('logger')

    def get(self):
        self.logger.info('Get status')
        db = Database()
        config = read_config()
        targets = json.load(open(config.get('targets')))
        for target in targets:
            self.logger.info('Getting status for "%s"', target['name'])
            target_logs = db.get_entries(target['target_id'], 1)
            if len(target_logs) == 0:
                target['code'] = -1
                target['checked'] = ''
                continue

            newest_log = target_logs[0]
            target['code'] = newest_log['code']
            target['checked'] = timestamp_to_string(newest_log['timestamp'])
            target['response_title'] = newest_log['response_title']
            if 'cookie_path' in target:
                del target['cookie_path']

            if 'url' in target:
                del target['url']

        self.logger.info('Return status for %d objects', len(targets))
        resp = flask.Response(json.dumps(targets))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Content-Type'] = 'application/json'
        return resp


class Logs(Resource):

    def __init__(self):
        self.logger = logging.getLogger('logger')

    def get(self, target_id=None, limit=25):
        self.logger.info('Get all logs')
        db = Database()
        all_logs = db.get_entries(target_id, limit)
        for log in all_logs:
            log['checked'] = timestamp_to_string(log['timestamp'])

        self.logger.info('Will return %d log entries', len(all_logs))
        resp = flask.Response(json.dumps(all_logs))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Content-Type'] = 'application/json'
        return resp
