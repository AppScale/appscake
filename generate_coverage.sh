#!/bin/sh
rm -rf coverage
rcov test/tc_appscake_utils.rb -x test/tc_appscake_utils.rb -x /var/lib/gems/
