RUN, STOP, STATUS AND RESTART INSTRUCTIONS

RUN SERVICE
  sudo systemctl start romi@shome.service

STOP SERVICE
  sudo systemctl stop romi@shome.service

STATUS SERVICE
  sudo systemctl status romi@shome.service

RESTART SERVICE
  sudo systemctl restart romi@shome.service

LOG
  tail -f /var/log/messages
