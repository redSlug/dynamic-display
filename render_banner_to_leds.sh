#!/bin/bash

# crontab -e
# @reboot /home/pi/weather-reporter/pi/show_weather.sh
# sed -i 's/BANNER_IMAGE_FILE="weather.ppm/BANNER_IMAGE_FILE="weather_2.ppm/g' /home/pi/weather-reporter/pi/show_weather.sh

MAX_LOG_FILE_SIZE=250000000
LOG_FILE=/home/pi/weather-reporter/pi/log
BANNER_IMAGE_FILE="weather_2.ppm"
POLLING_DELAY=2m
LED_DELAY_MS=18
#BANNER_PATH=http146.190.76.40
# http://206.189.229.207/static/$BANNER_IMAGE_FILE
BANNER_PATH=https://dynamicdisplay.recurse.com/static/weather_2.ppm



function log_to_file {
    echo "$(date) $1" >> log
}

function cleanup {
    log_to_file "Clearing LED display"
    sudo pkill led-image-viewer
    exit
}

function rotate_logs_if_needed {
    log_file_size=$(du -b log | tr -s '\t' ' ' | cut -d' ' -f1)

    if [ $log_file_size -gt $MAX_LOG_FILE_SIZE ];then
        log_to_file "Rotating log file of size $log_file_size bytes"
        mv $LOG_FILE "$LOG_FILE.backup"
        touch $LOG_FILE
    fi
}

function main {
    pushd /home/pi/weather-reporter/pi

    while true; do
        wget -N $BANNER_PATH
        if [ $? -eq 0 ];
        then
            log_to_file "wget succeeded"
            sudo pkill demo
            sudo rpi-rgb-led-matrix/utils/led-image-viewer --led-no-hardware-pulse --led-rows=16 --led-cols=32 --led-daemon --led-brightness=10 -f $BANNER_IMAGE_FILE
        else
            log_to_file "wget failed - file was likely not modified"

            if [ ! -f $BANNER_IMAGE_FILE ]; then
                log_to_file "File not found!"
                exit 1
            fi
        fi

        rotate_logs_if_needed
        sleep $POLLING_DELAY
    done

    popd
}

trap cleanup EXIT
main