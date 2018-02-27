#!/bin/bash

# Change code according to your own needs

# Init kerberos

kinit jrumsevi@CERN.CH -k -t /home/WebStatusMonitoring/jrumsevi.keytab

# Remove old cookies

rm /home/WebStatusMonitoring/cookies/prod-cookie
rm /home/WebStatusMonitoring/cookies/dev-cookie

# Create new cookies

cern-get-sso-cookie -u https://cms-pdmv.cern.ch/mcm/ -o /home/WebStatusMonitoring/cookies/prod-cookie --krb
cern-get-sso-cookie -u https://cms-pdmv-dev.cern.ch/mcm/ -o /home/WebStatusMonitoring/cookies/dev-cookie --krb

# Trigger an update

curl -s 'http://localhost:5000/update_status'
