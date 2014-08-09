#!/bin/bash
# uwsgi - Use uwsgi to run python and wsgi web apps.
#
# chkconfig: - 85 15
# description: Use uwsgi to run python and wsgi web apps.
# processname: uwsgi

CONF=/opt/yourwebsite.com/server_config/uwsgi.ini
PATH=/opt/uwsgi:/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/usr/bin/uwsgi

OWNER=root
NAME=uwsgi_yourwebsite.com
DESC=uwsgi_yourwebsite.com

pidfile=/var/run/${NAME}.pid

test -x $DAEMON || exit 0

# Include uwsgi defaults if available
if [ -f /etc/default/uwsgi ] ; then
        . /etc/default/uwsgi
fi

set -e

get_pid() {
    if [ -f $pidfile ]; then
        echo `cat $pidfile`
    fi
}

DAEMON_OPTS="--pidfile /var/run/$NAME.pid $CONF"

case "$1" in
  start)
        echo -n "Starting $DESC: "
        PID=$(get_pid)
        if [ -z "$PID" ]; then
            [ -f $pidfile ] && rm -f $pidfile

            touch $pidfile
            chown $OWNER $pidfile
            su - $OWNER -pc "$DAEMON $DAEMON_OPTS > /dev/null 2>&1 &"
            echo "$NAME."
        fi

        ;;
  stop)
        echo -n "Stopping $DESC: "
        PID=$(get_pid)
        [ ! -z "$PID" ] && kill -s 3 $PID &> /dev/null
        if [ $? -gt 0 ]; then
            echo "was not running" 
        else
            echo "$NAME."
            rm -f $pidfile &> /dev/null
        fi
        ;;

  reload)
        echo "Reloading $NAME" 
        PID=$(get_pid)
        [ ! -z "$PID" ] && kill -s 1 $PID &> /dev/null
        if [ $? -gt 0 ]; then
            echo "was not running" 
            exit 1
        else
            echo "$NAME."
            rm -f /var/run/$NAME.pid &> /dev/null
        fi
        ;;
  force-reload)
        echo "Reloading $NAME" 
        PID=$(get_pid)
        [ ! -z "$PID" ] && kill -s 15 $PID &> /dev/null
        if [ $? -gt 0 ]; then
            echo "was not running" 
            exit 1
        else
            echo "$NAME."
            rm -f /var/run/$NAME.pid &> /dev/null
        fi
        ;;
  restart)
        $0 stop
        sleep 2
        $0 start
        ;;
  status)
        killall -10 $DAEMON
        ;;
      *)
            N=/etc/init.d/$NAME
            echo "Usage: $N {start|stop|restart|reload|force-reload|status}" >&2
            exit 1
            ;;
    esac
    exit 0