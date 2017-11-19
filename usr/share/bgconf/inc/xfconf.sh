#!/bin/sh
# File: /usr/share/bgconf/inc/xfconf.sh
# Author: bgstack15
# Startdate: 2017-09-17 08:10
# Title: Script that Loads Settings into Xfconf
# Purpose: To make a single interface for other bgconf scripts to call for loading an xfconf file
# History:
#    2017-06 Main research was done but put in separate bgconf scripts.
#    2017-09-17 I decided to separate it out to streamline the bgconf scripts themselves.
#    2017-10-14 Updated how to find the running desktop environment
# Usage:
#    In a script, determine that an xfconf file exists, then call:
#       xfconf.sh mysettings.xfconf
#    To generate a new xfconf file, you can run:
#       xfconf-query -l | sed -r -e '/Channels:/d' | while read line; do xfconf-query -lv -c "${line}" | sed -r -e "s/^/${line} /"; done > outfile
# Reference:
# Improve:
#    find a list online of datatypes for the xfce schema and calculate the created datatypes that way.
# Document: Below this line

thisDE=xfce4
thisDEconf=xfconf-query
infile="${1}"

# get DBUS_SESSION_BUS_ADDRESS of first DE process of this user
# reference:  https://unix.stackexchange.com/questions/29128/how-to-read-environment-variables-of-a-process/29132#29132
tmpfile1="$( mktemp )"
if test -n "${SUDO_USER}"; then _user="${SUDO_USER}"; else _user="${USER}"; fi
cat /proc/$( ps -U "${_user}" -e -o pid,user:20,command:90 2>/dev/null | grep -E "${thisDE}-session(\s|$)" | awk '{print $1}' | sort | uniq | head -n1 )/environ 2>/dev/null | tr '\0' '\n' | grep -E "DBUS_SESSION_BUS_ADDRESS|DISPLAY" > "${tmpfile1}"
test -f "${tmpfile1}" && test $( grep -cE "(DBUS_SESSION_BUS_ADDRESS|DISPLAY)=.+" "${tmpfile1}" 2>/dev/null ) -ge 2 || echo "$0 error: Skipping ${thisDE}: Could not find current session." 1>&2
chmod +rx "${tmpfile1}" 2>/dev/null
. "${tmpfile1}"
/bin/rm -f "${tmpfile1}" 1>/dev/null 2>&1

# Assume infile exists as a file
if test -n "$( cat "${infile}" 2>/dev/null )" && test -x "$( which "${thisDEconf}" )" && ps -ef | grep -qE "${thisDE}" && test -n "${DBUS_SESSION_BUS_ADDRESS}";
then

   # get user of that directory
   thisowner="$( stat -c '%U' "${infile}" )"
   thisowneruid="$( stat -c '%u' "${infile}" )"

   # xfce custom configuration
   grep -viE '^\s*((#|;).*)?$' "${infile}" | while read channel attrib value;
   do

      # display output
      #printf "channel=%s\tattrib=%s\tvalue\%s\n" "${channel}" "${attrib}" "${value}"

      # provide data type. This needs to be researched before making a new .xfconf file.
      _thistype=string
      case "${attrib}" in
         *last-separator-position) _thistype=integer ;;
         *last-show-hidden|*misc-single-click) _thistype=bool ;;
      esac

      # make change
      sudo su - "${thisowner}" -c "DISPLAY=${DISPLAY} DBUS_SESSION_BUS_ADDRESS=${DBUS_SESSION_BUS_ADDRESS} ${thisDEconf} --create -t ${_thistype} -c ${channel} -p ${attrib} -s ${value}"

   done

fi
/bin/rm -f "${tmpfile1}" 2>/dev/null
