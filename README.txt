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
  tail -f /var/log/messages
  [input your password]
