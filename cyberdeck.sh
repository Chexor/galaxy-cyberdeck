#!/bin/bash

# Galaxy Cyberdeck Unified CLI
# Usage: cyberdeck {start|stop|restart|dashboard|update|status}

# Navigate to the project directory (ensure paths are correct)
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$PROJECT_DIR"

case "$1" in
    start|stop|restart|status|update)
        ./manage-node.sh "$1"
        ;;
    dashboard)
        echo "Launching Galaxy Cyberdeck Dashboard..."
        python3 client/read_sensors.py
        ;;
    *)
        echo -e "\033[95mGalaxy Cyberdeck CLI\033[0m"
        echo "Usage: cyberdeck {start|stop|restart|dashboard|update|status}"
        exit 1
esac
