#! /bin/sh
### BEGIN INIT INFO
# Provides: Flock Celery
# Required-Start: $remote_fs $syslog
# Required-Stop: $remote_fs $syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Flock Celery
# Description: This file starts and stops the Flock Celery workers
#
### END INIT INFO

case "$1" in
 start)
   start-stop-daemon --start --pidfile /var/run/flock_celery.pid --make-pidfile --chuid ubuntu --user ubuntu --exec /data/www/env/bin/python -- /data/www/flock/flock/run_celery.py -c /data/www/flock/configs/flock-production.json &
   echo 'Flock Celery Started'
   ;;
 stop)
   start-stop-daemon --stop --user ubuntu --chuid ubuntu --pidfile /var/run/flock_celery.pid
   echo 'Flock Celery Stopped'
   ;;
 *)
   echo "Usage: flock-celery  {start|stop}" >&2
   exit 3
   ;;
esac
