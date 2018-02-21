from flask_restful import Resource
import json
from database import Database
from utils import notify, get_random_string
import subprocess
import os.path
import os
import re
import time
import logging


class UpdateStatus(Resource):
    def __init__(self):
        self.cookie_files = {}
        self.logger = logging.getLogger('logger')

    def get_sso_cookie_file_name(self, cookie_url):
        if not cookie_url or cookie_url == '':
            return None

        if cookie_url in self.cookie_files:
            return self.cookie_files[cookie_url]
        else:
            cookie_file_name = get_random_string()
            while os.path.exists(cookie_file_name):
                cookie_file_name = get_random_string()

            args = ['cern-get-sso-cookie', '-u', '"' + cookie_url + '"', '-o', cookie_file_name, '--krb']
            args = ' '.join(args)
            subprocess.Popen(args, shell=True)
            while not os.path.exists(cookie_file_name):
                time.sleep(0.1)

            self.cookie_files[cookie_url] = cookie_file_name
            return cookie_file_name

    def make_request(self, url, cookie_url):
        self.logger.info('Will make request to %s' % (url))
        try:
            cookie_file_name = self.get_sso_cookie_file_name(cookie_url)
            self.logger.info('Cookie file name for %s is "%s"' % (url, cookie_file_name))
            args = ["curl", url, "-s", "-k", "-L", "-m", "60", "-w", "%{http_code}", "-o", "/dev/null"]
            if cookie_file_name:
                self.logger.info('Append cookie "%s" while making request to %s' % (cookie_file_name, url))
                args += ["--cookie", cookie_file_name]

            args = ' '.join(args)
            proc = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
            code = proc.communicate()[0]
            code = int(code)

            args = ["curl", url, "-s", "-k", "-L", "-m", "60"]
            if cookie_file_name:
                args += ["--cookie", cookie_file_name]

            args = ' '.join(args)
            proc = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
            output_title = str(proc.communicate()[0])
            m = re.search('<title>(.*?)</title>', output_title)
            if m:
                output_title = m.group(1)
                self.logger.info('Found title for %s. Title is "%s"' % (url, output_title))
            else:
                output_title = '<no title>'

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

        targets = json.load(open('targets.json'))
        updated_targets = []
        db = Database()
        for target in targets:
            if target_name is not None and target['target_id'] != target_name:
                continue

            code, output_title = self.make_request(target['url'], target.get('sso_cookie_url'))
            target['code'] = code
            target['output_title'] = output_title
            self.logger.info('Code for "%s" (%s) is %d' % (target['name'], target['url'], target['code']))
            db.add_entry_for_target(target)
            updated_targets.append(target)

        for cookie_url in self.cookie_files:
            try:
                os.remove(self.cookie_files[cookie_url])
            except OSError as ex:
                self.logger.error('Error deleting cookie file "%s" for "%s". Exception %s' % (self.cookie_files.get(cookie_url), cookie_url, ex))
                pass

        self.parse_statuses(updated_targets)
        return updated_targets

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
