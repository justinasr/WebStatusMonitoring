import subprocess
import string
import random
import configparser
import re

SIGNATURE = '\n\nSincerely,\nStatus checker at '


def get_color_for_code(code):
    if code == 200:
        # Green
        return '#87D37C'
    elif code == 0:
        # Red
        return '#EC644B'
    else:
        # Yellow
        return '#F5D76E'


def get_hostname():
    proc = subprocess.Popen(['hostname'], stdout=subprocess.PIPE)
    return proc.communicate()[0].decode('utf-8')


def notify(subject, text):
    text += SIGNATURE + get_hostname()
    p1 = subprocess.Popen(['echo', text], stdout=subprocess.PIPE)
    config = read_config()
    if 'email-recipients' in config:
        recipients = re.split(", ", config.get('email-recipients', ''))
        for recipient in recipients:
            subprocess.Popen(['mail',
                              '-s',
                              subject,
                              recipient],
                             stdin=p1.stdout,
                             stdout=subprocess.PIPE)


def get_random_string(length=10):
    return ''.join(random.choice(string.ascii_uppercase +
                                 string.digits) for _ in range(length))


def read_config(name='DEFAULT'):
    name = name.upper()
    config = configparser.ConfigParser()
    config.read('config.cfg')
    if name in config:
        return config[name]
    else:
        return None
