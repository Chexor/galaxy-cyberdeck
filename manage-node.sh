#!/bin/bash

# Galaxy Cyberdeck Master Manager (Runs on the Pi)
# Usage: ./manage-node.sh {start|stop|restart|status|update}

# Import config (we'll extract the IP from config.py)
NODE_IP=$(grep "PHONE_IP =" config.py | cut -d '"' -f 2)
NODE_PORT="8022"

# Remote paths
REMOTE_HOME="/data/data/com.termux/files/home"
REMOTE_MANAGE="$REMOTE_HOME/manage.sh"

case "$1" in
    start|stop|restart|status)
        echo "Sending $1 command to Node at $NODE_IP..."
        ssh -p $NODE_PORT $NODE_IP "$REMOTE_MANAGE $1"
        ;;
    update)
        echo "Updating Node at $NODE_IP with latest code..."
        # Push server script
        scp -P $NODE_PORT termux-node/sensor_server.py $NODE_IP:$REMOTE_HOME/sensor_server.py
        # Push manager script just in case
        scp -P $NODE_PORT termux-node/manage.sh $NODE_IP:$REMOTE_MANAGE
        # Set permissions
        ssh -p $NODE_PORT $NODE_IP "chmod +x $REMOTE_MANAGE"
        echo "Update complete. Restarting server..."
        ssh -p $NODE_PORT $NODE_IP "$REMOTE_MANAGE restart"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|update}"
        exit 1
esac
