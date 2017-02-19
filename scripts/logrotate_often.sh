#!/bin/sh

echo 'MAILTO=\"\"' > /etc/cron.d/appscale-every-5
echo '*/5 * * * * root /usr/sbin/logrotate /etc/logrotate.d/appscale*' >> /etc/cron.d/appscale-every-5
