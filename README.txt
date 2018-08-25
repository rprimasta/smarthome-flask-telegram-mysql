RUN, STOP, STATUS AND RESTART INSTRUCTIONS

RUN SERVICE
  sudo systemctl start romi@shome.service
  [input your password]

STOP SERVICE
  sudo systemctl stop romi@shome.service
  [input your password]

STATUS SERVICE
  sudo systemctl status romi@shome.service
  [input your password]

RESTART SERVICE
  sudo systemctl restart romi@shome.service
  [input your password]

LOG
  sudo tail -f /var/log/messages
  [input your password]

SERVICE SCRIPT
  nano /home/romi/service/romi@shome.service

#===================/home/romi/service/romi@shome.service======================
[Unit]
Description=Smart Home Romi at Port 6001

[Service]
Type=simple
ExecStart=/usr/bin/stdbuf -oL /usr/bin/python /home/romi/service/shome.py >/home/romi/service/stdout.log >/home/romi/service/stderr.log

[Install]
WantedBy=multi-user.target
#==============================================================================
