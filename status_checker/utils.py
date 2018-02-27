import subprocess
import string
import random

RECIPIENT = 'justinas.rumsevicius@cern.ch'
SIGNATURE = '\n\nSincerely,\nStatus checker at http://instance4:5000'


def get_color_for_code(code):
    if code == 200:
        # Green
        return '#87D37C'
    elif code == -1:
        # Red
        return '#EC644B'
    else:
        # Yellow
        return '#F5D76E'


def notify(subject, text, recipient=RECIPIENT):
    text += SIGNATURE
    p1 = subprocess.Popen(['echo', text], stdout=subprocess.PIPE)
    subprocess.Popen(['mail', '-s', subject, recipient], stdin=p1.stdout, stdout=subprocess.PIPE)


def get_random_string(length=10):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
