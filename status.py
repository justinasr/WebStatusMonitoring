from flask_restful import Resource
from database import Database
from utils import get_color_for_code
import json
import logging


class Status(Resource):

    def __init__(self):
        self.logger = logging.getLogger('logger')

    def get(self):
        self.logger.info('Get status')
        db = Database()
        targets = json.load(open('targets.json'))
        for target in targets:
            self.logger.info('Getting status for "%s"' % (target[name]))
            target_logs = db.get_entries(target['target_id'], 1)
            if len(target_logs) == 0:
                target['code'] = -1
                target['checked'] = ''
                target['color'] = ''
                continue

            newest_log = target_logs[0]
            target['code'] = newest_log['code']
            target['checked'] = newest_log['date'][:16]
            target['color'] = get_color_for_code(newest_log['code'])
            target['output_title'] = newest_log['output_title']

        self.logger.info('Return status for %d objects' % (len(targets)))
        return targets


class Logs(Resource):

    def __init__(self):
        self.logger = logging.getLogger('logger')

    def get(self, target_name=None, limit=25):
        self.logger.info('Get all logs')
        db = Database()
        all_logs = db.get_entries(target_name, limit)
        for log in all_logs:
            log['date'] = log['date'][:16]
            log['color'] = get_color_for_code(log['code'])

        self.logger.info('Will return %d log entries' % (len(all_logs)))
        return all_logs
