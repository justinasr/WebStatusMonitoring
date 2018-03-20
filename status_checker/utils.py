import subprocess
import string
import random
import configparser
import re
import sys

SIGNATURE = '\n\nSincerely,\nStatus checker at '


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
    if len(sys.argv) > 1:
        name = sys.argv[1].upper()
    else:
        name = 'DEFAULT'

    config = configparser.ConfigParser()
    config.read('config.cfg')
    if name in config:
        return config[name]
    else:
        return None
