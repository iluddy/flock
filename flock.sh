#!/bin/bash
#
# chkconfig: 35 90 12
# description: Tracker Runner
#
# Get function from functions library
. /etc/init.d/functions

# Start
start() {
    if running $1;
    then
        echo "Tracker Already Running"
        echo;
    else
        echo "Starting Tracker..."
        sudo python /home/ec2-user/tracker/app.py -c /home/ec2-user/tracker.json > /dev/null 2>&1 &
        ### Create the lock file ###
        touch /var/lock/subsys/tracker
        echo "Tracker Running"
        echo;
    fi
}

# Restart
stop() {
    if running $1;
    then
        echo "Stopping Tracker..."
        ps -aef | grep "sudo python /home/ec2-user/tracker/app.py" | awk '{print $2}' | xargs sudo kill > /dev/null 2>&1 &
        ### Remove the Lock File ###
        rm -f /var/lock/subsys/tracker
        echo "Tracker Stopped"
        echo;
    else
        echo "Tracker Not Running"
        echo;
    fi
}
# Status
status() {
    if running $1;
    then
        echo "Tracker Running"
        echo;
    else
        echo "Tracker Not Running"
        echo;
    fi
}

running() {
    if [ -f "/var/lock/subsys/tracker" ]
    then
        return 0
    else
        return 1
    fi
}

### main logic ###
"tracker" 80L, 1484C
