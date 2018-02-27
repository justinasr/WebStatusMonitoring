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
7. Run with `python main.py &` or `python3 main.py &` (add `&` so it would run in background)


#### Status checking

...

#### Links

/
/update_status
/update_status/<target id>
/get_logs
/get_logs/<count>
/get_status

#### Target list file

...
