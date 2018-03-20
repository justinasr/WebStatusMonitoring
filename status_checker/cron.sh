#!/bin/bash

# Change code according to your own needs

# Init kerberos

this_dir=$(cd $(dirname $0) && pwd)
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

if [[ $1 == "dev" ]]
then
    curl -s 'http://localhost:5000/update_status'
else
    curl -s 'http://localhost/update_status'
fi
