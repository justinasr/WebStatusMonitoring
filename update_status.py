from flask_restful import Resource
import json
import urllib2
from database import Database
import subprocess


class UpdateStatus(Resource):
    def __init__(self):
        pass

    def make_request(self, url):
        result = urllib2.urlopen(url)
        return result

    def get_code(self, url):
        try:
            code = self.make_request(url).getcode()
        except urllib2.HTTPError as ex:
            code = ex.code
        except Exception as ex:
            code = -1

        return code

    def notify(self, targets):
        msg = ""
        for target in targets:
            if target['code'] != 200:
                msg += '%s is not ok. It returned code %s. \n' % (target['name'], target['code'])

        if len(msg) == 0:
            return

        msg += '\n\nSincerely,\nCron job at http://instance4:5000'
        p1 = subprocess.Popen(["echo", msg], stdout=subprocess.PIPE)
        subprocess.Popen(["mail", "-s", "Some services are not ok", 'justinas.rumsevicius@cern.ch'], stdin=p1.stdout, stdout=subprocess.PIPE)

    def get(self, target_name=None):
        targets = json.load(open('targets.json'))
        updated_targets = []
        db = Database()
        for target in targets:
            if target_name is not None and target['target_id'] != target_name:
                continue

            target['code'] = self.get_code(target['url'])
            db.add_entry_for_target(target)

            updated_targets.append(target)

        self.notify(updated_targets)

        return str(updated_targets)
