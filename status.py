from flask import render_template, make_response
from flask_restful import Resource
from database import Database
import json


class Status(Resource):
    def __init__(self):
        pass

    def get_color_for_code(self, code):
        if code == 200:
            # Green
            return '#87D37C'
        elif code == -1:
            # Red
            return '#EC644B'
        else:
            # Yellow
            return '#F5D76E'

    def get(self):
        db = Database()
        targets = json.load(open('targets.json'))
        all_logs = []
        id_to_name = {}
        for target in targets:
            target_logs = db.get_entries_for_target(target['target_id'])
            newest_log = target_logs[0]
            target['code'] = newest_log['code']
            target['checked'] = newest_log['date'][:16]
            target['color'] = self.get_color_for_code(target['code'])
            id_to_name[target['target_id']] = target['name']

        all_logs = db.get_all_targets_entries(25)
        for log in all_logs:
            log['name'] = id_to_name.get(log['target_id'])
            log['date'] = log['date'][:16]
            log['color'] = self.get_color_for_code(log['code'])

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html', targets=targets, all_logs=all_logs), 200, headers)
