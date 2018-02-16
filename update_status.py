from flask_restful import Resource
import json
import urllib2
from database import Database
from utils import notify
import subprocess
import os.path

COOKIE_FILE = 'cookie.txt'
SSO_COOKIE_URL = 'https://cms-pdmv.cern.ch/mcm/'


class UpdateStatus(Resource):
    def __init__(self):
        pass

    def get_sso_cookie(self):
        if not os.path.exists(COOKIE_FILE):
            try:
                args = ['cern-get-sso-cookie', '-u', SSO_COOKIE_URL, '-o', COOKIE_FILE, '--krb']
                subprocess.Popen(args)
            except Exception as ex:
                print('Error getting cookie. Reason: %s' % (ex))

    def make_request(self, url):
        self.get_sso_cookie()
        try:
            args = ["curl", "-L", "-k", "-s", "--cookie", COOKIE_FILE, url, "-I", "-w", "%{http_code}", "-o", "/dev/null"]
            proc = subprocess.Popen(args, stdout=subprocess.PIPE)
            code = proc.communicate()[0]
            code = int(code)
        except urllib2.HTTPError as ex:
            code = ex.code
        except Exception as ex:
            code = -1

        print('%s returned %d' % (url, code))
        return code

    def get(self, target_name=None):
        targets = json.load(open('targets.json'))
        updated_targets = []
        db = Database()
        for target in targets:
            if target_name is not None and target['target_id'] != target_name:
                continue

            code = self.make_request(target['url'])
            target['code'] = code
            db.add_entry_for_target(target)
            updated_targets.append(target)

        self.parse_statuses(updated_targets)
        return updated_targets

    def parse_statuses(self, targets):
        message = ""
        for target in targets:
            if target['code'] != 200:
                message += '%s is not ok. It returned code %s. \n' % (target['name'], target['code'])

        if len(message) == 0:
            return

        subject = 'Some services are not ok'
        notify(subject, message)
