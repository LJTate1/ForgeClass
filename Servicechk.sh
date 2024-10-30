#!/bin/bash
services=("ssh" "apache2" "mysql")

for service in "${services[@]}; do
  if systemctl is-active --quiet "$service:";then
    echo "$service is running"
  else
    echo "$service is not running"
    read -p " Do you want to start the $service? : " choice
    echo $choice
    if [ "$choice" = "y" ]; then
      sudo systemctl start "$services"
      echo "$service started"
    fi
  fi
done
