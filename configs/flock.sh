#! /bin/sh
### BEGIN INIT INFO
# Provides: Flock
# Required-Start: $remote_fs $syslog
# Required-Stop: $remote_fs $syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Flock
# Description: This file starts and stops the Flock app
#
### END INIT INFO

case "$1" in
 start)
   start-stop-daemon --start --pidfile /var/run/flock.pid --make-pidfile --user root --exec /data/www/env/bin/python -- /data/www/flock/flock/app.py -c /data/www/flock/configs/flock-production.json > /tmp/flock_app 2>&1 &
   echo 'Flock Started'
   ;;
 stop)
   start-stop-daemon --stop --pidfile /var/run/flock.pid
   echo 'Flock Stopped'
   ;;
 *)
   echo "Usage: flock  {start|stop}" >&2
   exit 3
   ;;
esac