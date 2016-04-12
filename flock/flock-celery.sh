#! /bin/sh
### BEGIN INIT INFO
# Provides: Flock Celery
# Required-Start: $remote_fs $syslog
# Required-Stop: $remote_fs $syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Flock Celery
# Description: This file starts and stops Flock Celery process
#
### END INIT INFO

WWW_DIR=/data/www

case "$1" in
 start)
   /data/www/env/bin/python $WWW_DIR/flock/flock/run_celery.py -c $WWW_DIR/flock/flock-production.json > /tmp/flock_celery &
   echo 'Celery Started'
   ;;
 stop)
   ps -aef | grep "flock/run_celery.py" | awk '{print $2}' | xargs sudo kill > /tmp/flock_celery &
   echo 'Celery Stopped'
   ;;
 restart)
   ps -aef | grep "flock/run_celery.py" | awk '{print $2}' | xargs sudo kill > /tmp/flock_celery &
   sleep 3
   /data/www/env/bin/python $WWW_DIR/flock/flock/run_celery.py -c $WWW_DIR/flock/flock-production.json > /tmp/flock_celery &
   echo 'Celery Restarted'
   ;;
 *)
   echo "Usage: flock-celery  {start|stop|restart}" >&2
   exit 3
   ;;
esac
