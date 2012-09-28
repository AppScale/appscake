#!/bin/sh
rm -rf coverage
rcov test/tc_appscake_utils.rb -x test/tc_appscake_utils.rb -x /var/lib/gems/ -x /usr/local/lib/site_ruby/1.8/rubygems/gem_path_searcher.rb -x ~/.rvm -x /usr/local/appscale-tools
