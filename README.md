# WebStatusMonitoring

A service that checks whether webpages ar up (returning HTTP status code 200). If necessary, service can obtain a CERN SSO Cookie before making a request and use it to authenticate. All checks are saved in local SQLite database.

Project is is compatible with Python 2 and 3.

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
3. (*To be implemented*) Update config.cfg
5. Add entry (port 5000 or whatever you chose) to iptables using `iptables-save` and `iptables-restore`
6. (*Optional*) Set up a cronjob with `crontab -e`
7. Run status checker with `python main.py &` or `python3 main.py &` (add `&` so it would run in background)

#### Status checking

Status checking is performed in *update_status.py* file. Method performs a simple GET request to given URL. If specified in targets.json, add a cookie file. Response HTTP status code is saved in database along with timestamp and website title. Website title is obtained by parsing the HTML and getting the value between <title> tags. If no title can be found, <no title> value is used. Status checker makes two GET requests - one for the HTTP status code and another for the title.

#### Links

* */* - Basic homescreen using Jinja templates and bootstrap (basic, not pretty)
* */update_status* - Update status of all targets
* */update_status/<target id>* - Update status of certain target
* */get_logs* - Get list of all logs (default amount)
* */get_logs/<count>* - Get list of all logs (specified amount)
* */get_status* - Get status of all targets

#### Target list file

...
