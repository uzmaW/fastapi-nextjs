#!/bin/bash
set -e

# Start rsyslog
rsyslogd

# activate our virtual environment here
. /opt/pysetup/.venv/bin/activate

# You can put other setup logic here

# Evaluating passed command:
exec "$@"


