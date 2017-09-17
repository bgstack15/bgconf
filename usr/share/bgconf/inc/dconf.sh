#!/bin/sh
# File: /usr/share/bgconf/inc/dconf.sh
# Author: bgstack15
# Startdate: 2017-09-17 07:53
# Title: Script that Loads Settings into Dconf
# Purpose: To make a single interface for other bgconf scripts to call for loading a dconf file
# History:
#    2017-06 Main research was done but put in separate bgconf scripts.
#    2017-09-17 I decided to separate it out to streamline the bgconf scripts themselves.
# Usage:
#    In a script, determine that a dconf file exists, then call:
#       dconf.sh mysettings.dconf
#    To generate a new dconf file, you can run:
#       dconf dump / > outfile
# Reference:
# Improve:
#    If I ever need to, pass in thisDE. It is possible other desktop environments use dconf and I will need to grep for 'gnome-shell' or something.
# Document: Below this line

thisDE=cinnamon
thisDEconf=dconf
infile="${1}"

# get DBUS_SESSION_BUS_ADDRESS of first DE process of this user
# reference:  https://unix.stackexchange.com/questions/29128/how-to-read-environment-variables-of-a-process/29132#29132
tmpfile1="$( mktemp )"
#xargs --null --max-args=1 echo < /proc/$( ps -eu${USER} | grep -E "${thisDE}" | head -n1 | awk '{print $1}' )/environ | grep -E "DBUS_SESSION_BUS_ADDRESS|DISPLAY" > "${tmpfile1}"
find /proc/ -regextype grep -regex "/proc/$( ps -eu${USER} | grep -E "${thisDE}" | head -n1 | awk '{print $1}' )/environ" 2>/dev/null | xargs grep -E "DBUS_SESSION_BUS_ADDRESS|DISPLAY" > "${tmpfile1}"
test -f "${tmpfile1}" && test $( grep -cE "(DBUS_SESSION_BUS_ADDRESS|DISPLAY)=.+" "${tmpfile1}" 2>/dev/null ) -ge 2 || echo "$0 error: Could not find current ${thisDE} session. Did not work." 1>&2
chmod +rx "${tmpfile1}" 2>/dev/null
. "${tmpfile1}"
/bin/rm -f "${tmpfile1}" 1>/dev/null 2>&1

# Assume infile exists as a file
if test -n "$( cat "${infile}" 2>/dev/null )" && test -x "$( which "${thisDEconf}" )" && ps -ef | grep -qE "${thisDE}" && test -n "${DBUS_SESSION_BUS_ADDRESS}";
then

   # get user of that directory
   thisowner="$( stat -c '%U' "${infile}" )"
   thisowneruid="$( stat -c '%u' "${infile}" )"

   # cinnamon custom configuration
   sudo su - "${thisowner}" -c "cat ${infile} | DISPLAY=${DISPLAY} DBUS_SESSION_BUS_ADDRESS=${DBUS_SESSION_BUS_ADDRESS} ${thisDEconf} load / ;"

fi
/bin/rm -f "${tmpfile1}" 2>/dev/null
