#!/bin/bash

# Galaxy Cyberdeck Unified CLI (v2 - Nested Commands)
# Usage: cyberdeck {node|flash|camera|dashboard|help}

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$PROJECT_DIR"

# Extract Node IP from config
NODE_IP=$(grep "PHONE_IP =" config.py | cut -d '"' -f 2)

show_help() {
    cat << "EOF"
\033[95m
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
\033[0m
EOF
    echo -e "Usage: \033[1mcyberdeck {category} {command}\033[0m\n"
    echo "Categories:"
    echo "  node <cmd>    - Infrastructure: start, stop, restart, update, status"
    echo "  flash <on|off>- Hardware: Control phone flashlight"
    echo "  camera <snap> - Hardware: Take a remote snapshot"
    echo "  dashboard     - Interface: Launch live visual dashboard"
    echo "  help          - Documentation: Show this menu"
    echo -e "\nExamples:"
    echo "  cyberdeck node update"
    echo "  cyberdeck flash on"
    echo "  cyberdeck camera snap"
}

case "$1" in
    node)
        case "$2" in
            start|stop|restart|status|update)
                ./manage-node.sh "$2"
                ;;
            *)
                echo "Usage: cyberdeck node {start|stop|restart|status|update}"
                ;;
        esac
        ;;
    flash)
        case "$2" in
            on|off)
                echo "Turning torch $2..."
                curl -s "http://$NODE_IP:5000/torch/$2" > /dev/null
                ;;
            *)
                echo "Usage: cyberdeck flash {on|off}"
                ;;
        esac
        ;;
    camera)
        case "$2" in
            snap)
                FILENAME="snap_$(date +%Y%m%d_%H%M%S).jpg"
                echo "Capturing image to $FILENAME..."
                curl -s -o "$FILENAME" "http://$NODE_IP:5000/snapshot"
                echo "Done."
                ;;
            *)
                echo "Usage: cyberdeck camera {snap}"
                ;;
        esac
        ;;
    dashboard)
        echo "Launching Galaxy Cyberdeck Dashboard..."
        python3 client/read_sensors.py
        ;;
    help|--help|-h|"")
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        show_help
        exit 1
esac
