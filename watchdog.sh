#!/bin/bash
# yingjian-website HTTP server watchdog
# Keeps python http.server alive — auto-restarts if it dies
LOG="/tmp/yj_watchdog.log"
PIDFILE="/tmp/yj_server.pid"
PORT=8877
DIR="/home/tangguo/yingjian-website"

log() { echo "$(date '+%m-%d %H:%M:%S') [watchdog] $1" >> "$LOG"; }

start_server() {
    cd "$DIR"
    python3 -m http.server $PORT --bind 0.0.0.0 >> "$LOG" 2>&1 &
    echo $! > "$PIDFILE"
    log "Started PID $(cat $PIDFILE)"
}

kill_server() {
    if [ -f "$PIDFILE" ]; then
        kill $(cat "$PIDFILE") 2>/dev/null
        rm -f "$PIDFILE"
        log "Killed old server"
    fi
}

check() {
    if [ -f "$PIDFILE" ]; then
        pid=$(cat "$PIDFILE")
        if kill -0 "$pid" 2>/dev/null; then
            return 0  # alive
        fi
    fi
    return 1  # dead
}

while true; do
    if check; then
        # alive, do nothing
        :
    else
        log "Server dead, restarting..."
        kill_server
        start_server
    fi
    sleep 30
done
