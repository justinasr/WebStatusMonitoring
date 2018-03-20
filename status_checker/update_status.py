from flask_restful import Resource
import json
from database import Database
from utils import notify, read_config
import subprocess
import re
import logging
import flask
import datetime


class UpdateStatus(Resource):
    def __init__(self):
        self.cookie_files = {}
        self.logger = logging.getLogger('logger')

    def make_request(self, url, cookie_path):
        self.logger.info('Will make request to %s' % (url))
        try:
            args = ["curl", url, "-s", "-k", "-L", "-m", "60", "-w", "%{http_code}", "-o", "/dev/null"]
            if cookie_path:
                cookie_path = "cookies/" + cookie_path
                self.logger.info('Append cookie "%s" while making request to %s' % (cookie_path, url))
                args += ["--cookie", cookie_path]

            args = ' '.join(args)
            proc = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
            code = proc.communicate()[0]
            code = int(code)

            args = ["curl", url, "-s", "-k", "-L", "-m", "60"]
            if cookie_path:
                args += ["--cookie", cookie_path]

            args = ' '.join(args)
            proc = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
            output_title = str(proc.communicate()[0])
            m = re.search('<title>(.*?)</title>', output_title)
            if m:
                output_title = m.group(1)
                self.logger.info('Found title for %s. Title is "%s"' % (url, output_title))
            else:
                output_title = '<no title>'

            self.logger.info('Finished request to %s. Code: %d, title: "%s"' % (url, code, output_title))
        except Exception as ex:
            self.logger.error('Got exception while making a request to %s. Exception %s' % (url, ex))
            code = -1
            output_title = ''

        return (code, output_title)

    def get(self, target_name=None):
        if target_name:
            self.logger.info('Check "%s" status' % (target_name))
        else:
            self.logger.info('Check status for all targets')

        config = read_config()
        targets = json.load(open(config.get('targets', 'targets.json')))
        min_refresh_interval = config.getint('min-refresh-interval', 60)
        updated_targets = []
        db = Database()
        for target in targets:
            if target_name is not None and target['target_id'] != target_name:
                continue

            newest_entries = db.get_entries(target['target_id'], 1)
            if len(newest_entries) > 0:
                now = datetime.datetime.now()
                entry_date = datetime.datetime.strptime(newest_entries[0]['date'][:19], '%Y-%m-%d %H:%M:%S')
                delta = now - entry_date
                if delta.total_seconds() < min_refresh_interval:
                    continue

            code, output_title = self.make_request(target['url'], target.get('cookie_path'))
            target['code'] = code
            target['output_title'] = output_title
            self.logger.info('Code for "%s" (%s) is %d' % (target['name'], target['url'], target['code']))
            db.add_entry_for_target(target)
            updated_targets.append(target)

        self.parse_statuses(updated_targets)
        resp = flask.Response(json.dumps(updated_targets))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Content-Type'] = 'application/json'
        return resp

    def parse_statuses(self, targets):
        message = ""
        for target in targets:
            if target['code'] != 200:
                message += '%s is not ok. It returned code %s. \n' % (target['name'], target['code'])

        if len(message) == 0:
            self.logger.info('All services seem to be working. Will do nothing')
            return

        self.logger.info('Some services are broken, will notify')
        subject = 'Some services are not ok'
        notify(subject, message)
