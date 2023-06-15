#!/bin/bash

# Source the .env file
source ./.env

# Set default update frequency if not provided in the .env file
UPDATE_FREQUENCY=${UPDATE_FREQUENCY:-1}

# Log files
logs=(
  "/root/config/logs/appdaemon/access.log"
  "/root/config/logs/appdaemon/appdaemon.log"
  "/config/logs/appdaemon/home.log"
  "/root/config/logs/appdaemon/bedroom.log"
  "/root/config/logs/appdaemon/diag.log"
  "/root/config/logs/appdaemon/error.log"
  "/root/config/logs/appdaemon/lab.log"
  "/root/config/logs/appdaemon/up.log"
  "/root/config/logs/appdaemon/hall.log"
)

# Create a new window
tmux new-window -n 'HA Log Monitoring'

# Display the first log in the new window, using watch to monitor the log file
tmux send-keys "ssh ${REMOTE_USER}@${REMOTE_SERVER} 'watch -n ${UPDATE_FREQUENCY} \"tail -n 50 ${logs[0]}\"'" C-m

# Iterate through the rest of the log files and display each in a new pane, using watch to monitor the log file
for ((i = 1; i < ${#logs[@]}; i++)); do
  tmux split-window -v
  tmux select-layout tiled
  tmux send-keys "ssh ${REMOTE_USER}@${REMOTE_SERVER} 'watch -n ${UPDATE_FREQUENCY} \"tail -n 50 ${logs[$i]}\"'" C-m
done

# Focus back on the first pane
tmux select-pane -t 0

# Switch back to the previous window
# tmux switch-client -n
