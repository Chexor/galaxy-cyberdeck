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
    help|--help|-h)
        echo -e "\033[95m"
   _____       _                                  
  / ____|     | |                                 
 | |  __  __ _| | __ ___  ___   _                 
 | | |_ |/ _` | |/ _` \ \/ / | | |                
 | |__| | (_| | | (_| |>  <| |_| |                
  \_____|\__,_|_|\__,_/_/\_\\__, |                
   _____      _              __/ |           _    
  / ____|    | |            |___/ |         | |   
 | |    _   _| |__   ___ _ __ __| | ___  ___| | __
 | |   | | | | '_ \ / _ \ '__/ _` |/ _ \/ __| |/ /
 | |___| |_| | |_) |  __/ | | (_| |  __/ (__|   < 
  \_____\__, |_.__/ \___|_|  \__,_|\___|\___|_|\_\
         __/ |                                    
        |___/                                     
        \033[0m"
        echo -e "Usage: \033[1mcyberdeck {command}\033[0m\n"
        echo "Commands:"
        echo "  start      - Start the sensor server on the phone (background)"
        echo "  stop       - Stop the sensor server on the phone"
        echo "  restart    - Restart the sensor server on the phone"
        echo "  status     - Check if the phone server is currently running"
        echo "  dashboard  - Launch the live visual telemetry dashboard"
        echo "  update     - Push latest local code to phone and restart server"
        echo "  help       - Show this help menu"
        ;;
    *)
        $0 help
        exit 1
esac
