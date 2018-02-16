from flask_restful import Resource
from database import Database
from utils import get_color_for_code
import json


class Status(Resource):

    def get(self):
        db = Database()
        targets = json.load(open('targets.json'))
        for target in targets:
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

        return targets


class Logs(Resource):

    def get(self, target_name=None, limit=25):
        db = Database()
        all_logs = db.get_entries(target_name, limit)
        for log in all_logs:
            log['date'] = log['date'][:16]
            log['color'] = get_color_for_code(log['code'])

        return all_logs
