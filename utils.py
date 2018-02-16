import subprocess


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


def notify(targets):
    msg = ""
    for target in targets:
        if target['code'] != 200:
            msg += '%s is not ok. It returned code %s. \n' % (target['name'], target['code'])

    if len(msg) == 0:
        return

    msg += '\n\nSincerely,\nCron job at http://instance4:5000'
    p1 = subprocess.Popen(["echo", msg], stdout=subprocess.PIPE)
    subprocess.Popen(["mail", "-s", "Some services are not ok", 'justinas.rumsevicius@cern.ch'], stdin=p1.stdout, stdout=subprocess.PIPE)
