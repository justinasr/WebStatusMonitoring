#!/bin/bash

this_dir=$(cd $(dirname $0) && pwd)
cd $this_dir/vue_wsm
npm run build
cp -R dist/* ../status_checker/templates