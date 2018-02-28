#!/bin/bash

# Change code according to your own needs

# Init kerberos

this_dir=/home/WebStatusMonitoring/status_checker
keytab_file_name=$(ls -A1 $this_dir | grep .keytab | head -n1)

echo 'Using '$this_dir/$keytab_file_name

kinit $USER@CERN.CH -k -t $this_dir/$keytab_file_name

# Remove old cookies

rm $this_dir/cookies/prod.cookie
rm $this_dir/cookies/dev.cookie

# Create new cookies

cern-get-sso-cookie -u https://cms-pdmv.cern.ch/mcm/ -o $this_dir/cookies/prod.cookie --krb
cern-get-sso-cookie -u https://cms-pdmv-dev.cern.ch/mcm/ -o $this_dir/cookies/dev.cookie --krb

# Trigger an update

curl -s 'http://localhost/update_status'
