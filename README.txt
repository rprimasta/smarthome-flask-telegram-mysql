RUN, STOP, STATUS AND RESTART INSTRUCTIONS

RUN SERVICE
  sudo systmctl start romi@shome.service

STOP SERVICE
  sudo systmctl stop romi@shome.service

STATUS SERVICE
  sudo systmctl status romi@shome.service

RESTART SERVICE
  sudo systmctl restart romi@shome.service

LOG
  tail -f /var/log/messages
