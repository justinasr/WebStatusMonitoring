import subprocess
import string
import random
try:
    import configparser
except:
    import ConfigParser as configparser
import re
import sys
import time

SIGNATURE = '\n\nSincerely,\nStatus checker at '
CONFIG = None


def get_hostname():
    proc = subprocess.Popen(['hostname'], stdout=subprocess.PIPE)
    return proc.communicate()[0].decode('utf-8')


def notify(subject, text):
    text += SIGNATURE + get_hostname()
    p1 = subprocess.Popen(['echo', text], stdout=subprocess.PIPE)
    config = read_config()
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


def read_config():
    global CONFIG
    if CONFIG is not None:
        return CONFIG

    if len(sys.argv) > 1:
        name = sys.argv[1].upper()
    else:
        name = 'DEFAULT'

    config = configparser.ConfigParser()
    config.read('config.cfg')
    CONFIG = dict(config.items(name))
    return CONFIG


def timestamp_to_string(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
