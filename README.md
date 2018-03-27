# WebStatusMonitoring

A service that checks whether webpages ar up (returning HTTP status code 200). If necessary, service can use a cookie, specified in configuration file. All checks are saved in local SQLite database.

Project is is compatible with Python 3.

#### Getting started
1. Clone this project
```
git clone https://github.com/justinasr/WebStatusMonitoring.git
```
2. Install flask and flask_restful using `pip`
```
sudo pip install flask
sudo pip install flask_restful
```
3. Update config.cfg
4. Update targets.json
5. Add entry (port 80, 5000 or other) to iptables using `iptables-save` and `iptables-restore`
6. (*Optional*) Set up a cronjob with `crontab -e`
7. Enter *status_checker* directory with `cd status_checker`
8. Run status checker with `python3 main.py &` (add `&` so it would run in background). If you want to run a specific config, put it after *main.py*, e.g. `python3 main.py DEV &`, otherwise *DEFAULT* config will be used.

#### Status checking

Status checking is performed in *status_checker/update_status.py* file. Checker performs a simple GET request to given URL. If specified in targets file, adds a cookie file with *--cookie*. Response HTTP status code is saved in database along with timestamp and website title. Website title is obtained by parsing the HTML and getting the *<title>* value. If no title can be found, *<no title>* value is used. At the moment, status checker makes two GET requests - one for the HTTP status code and another for the title. Responses are saved in local SQLite database. Consecutive call to the same target can be performed only every X seconds, specified as *min-refresh-interval* in config file.

If any of the status codes are not 200, email is sent with list of targets that return something else than OK.

#### Cron job

If cron job is set up, checker will check status of targets automatically. *status_checker/cron.sh* is just an example, used in one particular case at CERN.

#### Config file

Config file contains these fields:

* *port* - Port on which service will be running
* *email-recipients* - Recipients of email when target is not 100% ok
* *debug-mode* - Debug mode
* *targets* - JSON file with target list
* *min-refresh-interval* - Minimum amount of seconds between two consecutive target checks

#### Target file

Target file contains JSON list with objects that contain these fields:

* *name* - Name of target
* *url* - URL of target
* *target_id* - Unique ID for target (It must be unique!)
* *cookie_path* - (*Optional*) Name of cookie file in *status_checker/cookies* directory.

#### Links

* */* - Homescreen
* */simple* - Basic homescreen using Jinja templates and bootstrap (basic, not pretty)
* */update_status* - Update status of all targets
* */update_status/\<target id\>* - Update status of certain target
* */get_logs* - Get list of all logs (default amount)
* */get_logs/\<count\>* - Get list of all logs (specified amount)
* */get_status* - Get status of all targets

Note: If target has status code -1, it means target was never checked, if 0 - error while accessing target.
