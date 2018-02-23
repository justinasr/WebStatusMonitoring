#!/bin/bash

kinit jrumsevi@CERN.CH -f -k -t keytab.keytab

rm /home/WebStatusMonitoring/cookies/prod-cookie
rm /home/WebStatusMonitoring/cookies/dev-cookie

cern-get-sso-cookie -u https://cms-pdmv.cern.ch/mcm/ -o /home/WebStatusMonitoring/cookies/prod-cookie --krb
cern-get-sso-cookie -u https://cms-pdmv-dev.cern.ch/mcm/ -o /home/WebStatusMonitoring/cookies/dev-cookie --krb

curl -s 'http://localhost:5000/update_status'
