#!/bin/sh

# DEFINE FUNCTIONS

clean_mgm() {
   rm -rf "${MGM_TMPDIR}" 2>/dev/null
}

update_grub_if_changed() {
   # call: update_grub_if_changed "${MGM_INFILE}" "${MGM_TMPFILE1}"

   local infile="${1}"
   local tmpfile="${2}"

   # determine if changes were made to the file
   if diff -q "${infile}" "${tmpfile}" 2>&1 | grep -qiE 'differ' ;
   then
      # changes were made
      if fistruthy "${MGM_APPLY}" ;
      then
         sudo /bin/cp -p "${tmpfile}" "${infile}"
         sudo /usr/sbin/grub2-mkconfig -o "${MGM_GRUB_FILE:-/boot/grub2/grub.cfg}"
      fi
   else
      # no changes
      :
   fi

}

add_value_to_grub_line() {
   # call: add_value_to_grub_line "${MGM_TMPFILE1}" "GRUB_CMDLINE_LINUX" "quiet"

   local infile="${1}"
   local thisvar="${2}"
   local thisvalue="${3}"

   sed -i -r -e "/^${thisvar}=/{ /${thisvalue}/! { s/\"\s*\$/${thisvalue}\"/; } ; }" "${infile}"

}

remove_value_from_grub_line() {
   # call: remove_value_from_grub_line "${MGM_TMPFILE1}" "GRUB_CMDLINE_LINUX" "quiet"

   local infile="${1}"
   local thisvar="${2}"
   local thisvalue="${3}"

   sed -i -r -e "/^${thisvar}=/{ /${thisvalue}/ { s/\s*${thisvalue}//; } ; }" "${infile}"

}

# REACT TO OS
# fail out if not rhel-based
. /usr/share/bgscripts/framework.sh
case "${thisflavor}" in
   fedora|el|centos|korora) : ;;
   *) exit 0 ;;
esac

# set variables
test -z "${MGM_TMPDIR}" && MGM_TMPDIR="$( mktemp -d )"
test -z "${MGM_TMPFILE1}" && MGM_TMPFILE1="$( TMPDIR="${MGM_TMPDIR}" mktemp )"

test -z "${MGM_INFILE}" && MGM_INFILE=/etc/default/grub
test -z "${MGM_GRUB_FILE}" && MGM_GRUB_FILE=/boot/grub2/grub.cfg
test -z "${MGM_APPLY}" && MGM_APPLY=yes
test -z "${MGM_RHGB}" && MGM_RHGB=no
test -z "${MGM_QUIET}" && MGM_QUIET=no

# clean up temp file if necessary
test ! -e "${MGM_TMPFILE1}" && { touch "${MGM_TMPFILE1}" || exit 1 ; }
cat "${MGM_INFILE}" > "${MGM_TMPFILE1}"
trap '__ec=$? ; clean_mgm ; trap "" 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 ; exit ${__ec:-0} ;' 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20

# Do the RHGB action
if fistruthy "${MGM_RHGB}" ;
then
   # add rhgb to grub config
   add_value_to_grub_line "${MGM_TMPFILE1}" "GRUB_CMDLINE_LINUX" "rhgb"
else
   # remove rhgb
   remove_value_from_grub_line "${MGM_TMPFILE1}" "GRUB_CMDLINE_LINUX" "rhgb"
fi

# Do the QUIET action
if fistruthy "${MGM_QUIET}" ;
then
   # add quiet to grub config
   add_value_to_grub_line "${MGM_TMPFILE1}" "GRUB_CMDLINE_LINUX" "quiet"
else
   # remove quiet
   remove_value_from_grub_line "${MGM_TMPFILE1}" "GRUB_CMDLINE_LINUX" "quiet"
fi

# Determine if any changes occurred to the file
update_grub_if_changed "${MGM_INFILE}" "${MGM_TMPFILE1}"

# show final results
fistruthy "${MGM_VERBOSE}" && cat "${MGM_TMPFILE1}"
