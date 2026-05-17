#!/data/data/com.termux/files/usr/bin/bash

# Galaxy Cyberdeck Service Manager
# Usage: ./manage.sh {start|stop|restart|status|logs}

SERVER_SCRIPT="$HOME/sensor_server.py"
LOG_FILE="$HOME/server.log"

case "$1" in
    start)
        if pgrep -f "python $SERVER_SCRIPT" > /dev/null; then
            echo "Server is already running."
        else
            # Log Rotation: If log is > 1MB, move it to .old
            if [ -f "$LOG_FILE" ]; then
                FILE_SIZE=$(stat -c%s "$LOG_FILE")
                if [ "$FILE_SIZE" -gt 1048576 ]; then
                    echo "Log file too large ($FILE_SIZE bytes). Rotating..."
                    mv "$LOG_FILE" "${LOG_FILE}.old"
                fi
            fi

            echo "Starting Galaxy Cyberdeck Server..."
            # Ensure SSH is running for future management
            if ! pgrep sshd > /dev/null; then
                echo "Starting SSH server..."
                sshd -p 8022
            fi
            nohup python "$SERVER_SCRIPT" > "$LOG_FILE" 2>&1 &
            echo "Server started in background. Logs: $LOG_FILE"
        fi
        ;;
    stop)
        echo "Stopping server..."
        pkill -f "python $SERVER_SCRIPT"
        echo "Server stopped."
        ;;
    restart)
        $0 stop
        sleep 1
        $0 start
        ;;
    status)
        if pgrep -f "python $SERVER_SCRIPT" > /dev/null; then
            PID=$(pgrep -f "python $SERVER_SCRIPT")
            echo "Server is RUNNING (PID: $PID)"
            echo "Last 5 log entries:"
            tail -n 5 "$LOG_FILE"
        else
            echo "Server is STOPPED."
        fi
        ;;
    logs)
        echo "Showing live logs (Press Ctrl+C to stop viewing)..."
        tail -f "$LOG_FILE"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        exit 1
esac
