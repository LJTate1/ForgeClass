#!/bin/bash
echo "For Loop Example"
echo
backup_dir="/tmp/backup_$(date +%Y%m%d_%H%S) "
mkdir -p "$backup_dir"
for file in "$HOME/*"{txt,py,md,\sh};do
  [ -e "$file" ] || continue
    cp "$file" "$backup_dir"
    done
echo "Backup created in $backup_dir"    
    
