#!/bin/sh
# File: /usr/share/bgconf/xfce.sh
# Author: bgstack15
# Startdate: 2017-09-17 07:43
# Title: Script that Deploys Bgconf to an Xfce client
# Purpose: Properly deploys bgconf to an xfce client
# History:
# Usage: As regular user, run /usr/share/bgconf/xfce.sh
# Reference:
# Improve:
# Document: Below this line

# Define functions
fatal_error() {
   echo "$0: Error. Run this as normal user. Aborted."
   exit 1
}

# Detect if root or sudo user
case "${SUDO_USER}" in
   "") :;;
   *) fatal_error;;
esac
case "${USER}" in
   "root") fatal_error;;
   *) :;;
esac

rm -rf ~/.config/xfce4
sudo /usr/share/bgconf/bgconf.py
if test -e "$( which loginctl 2>/dev/null )";
then
   loginctl kill-user ${USER}
else
   echo "Please log out immediately."
fi
