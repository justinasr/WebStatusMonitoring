from flask_restful import Resource
import json
import urllib2
from database import Database
from utils import notify


class UpdateStatus(Resource):
    def __init__(self):
        pass

    def make_request(self, url):
        try:
            response = urllib2.urlopen(url)
            code = response.getcode()
            output = response.read()
            response.close()
        except urllib2.HTTPError as ex:
            code = ex.code
            output = ''
        except Exception as ex:
            code = -1
            output = ''

        return (code, output)

    def get(self, target_name=None):
        targets = json.load(open('targets.json'))
        updated_targets = []
        db = Database()
        for target in targets:
            if target_name is not None and target['target_id'] != target_name:
                continue

            code, output = self.make_request(target['url'])
            target['code'] = code
            target['output'] = output
            db.add_entry_for_target(target)
            target['output'] = len(output)
            updated_targets.append(target)

        notify(updated_targets)

        return updated_targets
