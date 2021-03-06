#! /bin/sh
### BEGIN INIT INFO
# Provides: Flock
# Required-Start: $remote_fs $syslog
# Required-Stop: $remote_fs $syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Flock
# Description: This file starts and stops Flock app
#
### END INIT INFO

WWW_DIR=/data/www

case "$1" in
 start)
   /data/www/env/bin/python $WWW_DIR/flock/flock/app.py -c $WWW_DIR/flock/flock-production.json > /tmp/flock_service &
   echo 'Flock Started'
   ;;
 stop)
   ps -aef | grep "flock/app.py" | awk '{print $2}' | xargs sudo kill > /tmp/flock_service &
   echo 'Flock Stopped'
   ;;
 restart)
   ps -aef | grep "flock/app.py" | awk '{print $2}' | xargs sudo kill > /tmp/flock_service &
   sleep 3
   /data/www/env/bin/python $WWW_DIR/flock/flock/app.py -c $WWW_DIR/flock/flock-production.json > /tmp/flock_service &
   echo 'Flock Restarted'
   ;;
 *)
   echo "Usage: flock  {start|stop|restart}" >&2
   exit 3
   ;;
esac
