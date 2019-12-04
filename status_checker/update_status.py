from flask_restful import Resource
from database import Database
from utils import send_email, read_config, setup_console_logging, make_request
import json
import re
import logging
import flask
import time


class UpdateStatus(Resource):
    def __init__(self):
        self.cookie_files = {}
        self.logger = logging.getLogger('logger')
        self.db = Database()

    def get(self, target_id=None):
        if target_id:
            self.logger.info(f'Check "{target_id}" status')
        else:
            self.logger.info('Check status for all targets')

        config = read_config()
        response_dict = self.check(config, target_id)
        resp = flask.Response(json.dumps(response_dict, indent=2))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Content-Type'] = 'application/json'
        return resp

    def check(self, config, check_target_with_id=None):
        all_targets = json.load(open(config.get('targets')))
        if check_target_with_id is not None:
            all_targets = [x for x in all_targets if x['target_id'] == check_target_with_id]

        min_refresh_interval = int(config.get('min-refresh-interval', 60))
        updated_targets = []
        broken_target_messages = []
        returned_target_messages = []
        self.logger.info('Found %s targets', len(all_targets))
        for target in all_targets:
            target_url = target['url']
            target_name = target['name']
            previous_code = -1
            newest_entries = self.db.get_entries(target['target_id'], 1)
            if len(newest_entries) > 0:
                now = time.time()
                last_entry_timestamp = newest_entries[0]['timestamp']
                previous_code = newest_entries[0]['code']
                if now - last_entry_timestamp < min_refresh_interval:
                    self.logger.info('Not checking %s because it was checked less than %s seconds ago',
                                     target_name,
                                     min_refresh_interval)
                    continue

            self.logger.info('Will make request to %s', target_url)
            try:
                target_cookie = target.get('cookie_path')
                if target_cookie:
                    target_cookie = f'cookies/{target_cookie}'

                code, response = make_request(target_url, target_cookie)
                re_result = re.search('<title>(.*?)</title>', response)
                if re_result:
                    response_title = re_result.group(1)
                    self.logger.info('Found title for %s. Title is "%s"', target_url, response_title)
                else:
                    response_title = '<no title>'

                self.logger.info('Finished request to %s. Code: %d, title: "%s"', target_url, code, response_title)
            except Exception as ex:
                self.logger.error('Got exception while making a request to %s. Exception %s', target_url, ex)
                code = 0
                response_title = ''

            target['code'] = code
            target['response_title'] = response_title
            self.logger.info('Code for "%s" (%s) is %d, title %s',
                             target_name,
                             target_url,
                             code,
                             response_title)
            self.db.add_entry_for_target(target)
            updated_targets.append(target)
            if code != previous_code:
                if code < 200 or code > 299:
                    broken_target_messages.append(f'{target_name} is not OK. Code {code} and title {response_title}')
                else:
                    returned_target_messages.append(f'{target_name} is OK again. Code {code} and title {response_title}')

        self.notify(config, broken_target_messages, returned_target_messages)
        return updated_targets

    def notify(self, config, broken_target_messages, returned_target_messages):
        recipients = [x.strip() for x in config.get('email-recipients', '').split(',')]
        if broken_target_messages:
            subject = 'PdmV services are not OK'
            message = 'Hello,\n\nThese PdmV services are not working:\n\n'
            message += '\n'.join(broken_target_messages)
            message += '\n\nSincerely,\nPdmV status checker at https://cms-pdmv.cern.ch/status'
            self.logger.info('%s\n%s', subject, message)
            send_email(subject, message, recipients)

        if returned_target_messages:
            subject = 'PdmV services are back'
            message = 'Hello,\n\nThese PdmV services are working again:\n\n'
            message += '\n'.join(returned_target_messages)
            message += '\n\nSincerely,\nPdmV status checker at https://cms-pdmv.cern.ch/status'
            self.logger.info('%s\n%s', subject, message)
            send_email(subject, message, recipients)


if __name__ == '__main__':
    setup_console_logging()
    UpdateStatus().get()
