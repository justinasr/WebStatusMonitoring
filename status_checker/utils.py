import subprocess
import configparser
import sys
import time
import urllib.request
import logging
import http.cookiejar as cookielib
import logging.handlers


CONFIG = None
__LOG_FORMAT = '[%(asctime)s][%(levelname)s] %(message)s'


def make_request(url, cookie=None, timeout=60):
    """
    Make a request to given url
    Retur a code and string response
    """
    if cookie:
        cookie_jar = cookielib.MozillaCookieJar(cookie)
        cookie_jar.load()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    else:
        opener = urllib.request.build_opener()

    logger = logging.getLogger('logger')
    headers = {'User-Agent': 'McM Scripting'}
    request = urllib.request.Request(url, headers=headers, method='GET')
    logger.info(f'Making request to {url}')
    try:
        response = opener.open(request, timeout=timeout)
        code = response.getcode()
        response = response.read()
        response = response.decode('utf-8')
        logger.info(f'Status {code} for {url}')
        return (code, response)
    except urllib.error.HTTPError as ex:
        # HTTP error code - 400, 500
        code = ex.code
        reason = ex.reason
        logger.warning(f'HTTP error {code} while making a request to {url}. Reason: {reason}')
        return (code, f'<title>{ex.reason}</title>')
    except:
        logger.error(f'Error while making a request to {url}.')
        return 0, ''


def send_email(subject, text, recipients):
    p1 = subprocess.Popen(['echo', text], stdout=subprocess.PIPE)
    for recipient in recipients:
        subprocess.Popen(['mail',
                          '-s',
                          subject,
                          recipient],
                         stdin=p1.stdout,
                         stdout=subprocess.PIPE)


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


def setup_console_logging():
    logger = logging.getLogger('logger')
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(fmt=__LOG_FORMAT, datefmt='%d/%b/%Y:%H:%M:%S')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def setup_file_logging():
    # Max log file size - 5Mb
    max_log_file_size = 1024 * 1024 * 5
    max_log_file_count = 5
    log_file_name = 'logs.log'
    logger = logging.getLogger('logger')
    logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(log_file_name,
                                                   'a',
                                                   max_log_file_size,
                                                   max_log_file_count)
    formatter = logging.Formatter(fmt=__LOG_FORMAT, datefmt='%d/%b/%Y:%H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def timestamp_to_string(timestamp):
    return time.strftime('%Y-%m-%d %H:%M', time.localtime(timestamp))
