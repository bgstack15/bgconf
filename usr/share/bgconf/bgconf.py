#!/usr/bin/python3
# File: /usr/share/bgconf/bgconf.py
# Author: bgstack15@gmail.com
# Startdate: 2017-04-06 21:46
# Title: Script that Deploys My Conf Files
# Purpose: Deploys confs for applications that exist on this system
# History:
# Usage:
# Reference:
#    https://bgstack15.wordpress.com/2017/04/06/add-extension-to-firefox-as-default/
#    scrub.py
#    Innumerable official python3 docs
#    simple custom config parsing http://www.decalage.info/en/python/configparser
#    remove non-digit characters from string https://geonet.esri.com/thread/63201
#    split line but keep quotes http://stackoverflow.com/a/79989/3569534
# Improve:
# Dependencies:
#    python3

from __future__ import print_function
import argparse, os, sys, re, shlex, shutil, subprocess
import localapp

# BGCONF VERSION
bgconfpyversion = "2017-04-10a"

# DEFINE FUNCTIONS
def ferror(*args, **kwargs):
   print(*args, file=sys.stderr, **kwargs)

def istruthy(valtocheck):
   _value = False
   if str(valtocheck).lower() in ['1','y','yes','true','always']: _value = True
   return _value

def debuglev(_numbertocheck):
   # if _numbertocheck <= debuglevel then return truthy
   _debuglev = False
   try:
      if int(_numbertocheck) <= int(debuglevel):
         _debuglev = True
   except Exception as e:
      pass
   return _debuglev

def copyifactive(_filetype, _source, _dest, _thisapp):
   # use the _thisapp.force, .overwrite options
   _doit = False
   _source = standard_replacements(_source, _thisapp)
   _dest = standard_replacements(_dest, _thisapp)
   if os.path.isfile(_dest) and ( _thisapp.overwrite or overwriteall ) or not os.path.isfile(_dest): _doit = True
   if _doit:
      try:
         os.path.isdir(os.path.dirname(_dest))
      except:
         os.makedirs(os.path.dirname(_dest))
      if debuglev(1) and dryrun: ferror("Please copy " + _source + " to " + _dest)
      if _filetype == "file":
         if not dryrun:
            shutil.copy2(_source,_dest)
            if debuglev(1): ferror("Copied " + _source + " to " + _dest)
            _needaction=True
      else:
         # assume directory
         try:
            shutil.rmtree(_dest)
         except:
            pass
         if not dryrun:
            shutil.copytree(_source,_dest)
            _needaction=True
            if debuglev(1): ferror("Copied " + _source + " to " + _dest)
      # Bonus: set permissions for files in a home directory
      if re.compile('^(\/home\/).*').match(_dest):
         _split = _dest.split('/')
         _homedirstr = '/' + _split[1] + '/' + _split[2]
         _homedir = os.stat(_homedirstr)
         _owner = _homedir.st_uid
         _group = _homedir.st_gid
         #try:
         for _rootdir, _dirs, _files in os.walk(_dest):
            os.chown(_rootdir, _owner, _group)
            for _object in _dirs:
               os.chown(os.path.join(_rootdir, _object), _owner, _group)
            for _object in _files:
               os.chown(os.path.join(_rootdir, _object), _owner, _group)
         #except:
         #   pass

def act(_act, _thisapp):
   if istruthy(_needaction):
      if debuglev(1): ferror("Execute " + _act)
      subprocess.call(_act.split())
   else:
      if debuglev(1): ferror("Skipping action " + _act)

def standard_replacements(_string, _thisapp):
   try:
      _home = os.path.expanduser('~' + os.environ['SUDO_USER'])
   except:
      try:
         _home = os.path.expanduser('~bgirton')
         _os.path.exists(_home)
      except:
         try:
            _home = os.path.expanduser('~bgirtonvm')
            _os.path.exists(_home)
         except:
            try:
               _home = os.path.expanduser('~bgirton-local')
               _os.path.exists(_home)
            except:
               _home = os.path.expanduser('~')

   substitutions = {
      '${USERHOME}': os.path.expanduser('~'),
      '${HOME}': _home,
      '${BGHOME}': '/home/bgirton',
      '${defaultsource}': zones['default'].source,
      '${source}': _thisapp.source,
      '${app}': _thisapp.name, '${application}': _thisapp.name,
      }
   for _name, _item in substitutions.items():
      _string = _string.replace(_name, _item)
   for _name, _item in substitutions.items():
      _string = _string.replace(_name, _item)
   return os.path.normpath(_string)

# DEFINE DEFAULT VARIABLES
conffile = "/usr/share/bgconf/bgconf.conf"
scriptname = "bgconf"
forceall = ""
overwriteall = ""
dryrun = False
debuglevel = 0

# READ COMMAND LINE ARGUMENTS
parser = argparse.ArgumentParser(description="Deploy bgconfs for applications on localhost")
parser.add_argument("-d","--debug", nargs='?', default=0, type=int, choices=range(0,11), help="Set debug level.")
parser.add_argument("-V","--version", action="version", version="%(prog)s " + bgconfpyversion)
parser.add_argument("-f","--force", action="store_true", help="Force deploy all confs.")
parser.add_argument("-b","--backup", action="store_true", help="Force backup of all confs.")
parser.add_argument("-c","--conf","--config", action="store", help="Use this conf instead of default " + conffile)
parser.add_argument("-r","--dry","--dryrun","--dry-run", action="store_true", help="Do not execute. Useful when debugging.")
args = parser.parse_args()
if args.debug is None:
   debuglevel = 5
elif args.debug:
   debuglevel = args.debug

if debuglev(1): ferror("debug level", debuglevel )

DEBUG_LINES_RAW = 9
DEBUG_LINES = 8
DEBUG_OPTIONS = 4
DEBUG_EXECUTE = 1

# SELECT CONFIG FILE
# select config file after cli because cli might define config file
if args.conf is not None:
   if os.path.isfile(args.conf):
      conffile = args.conf
   else:
      ferror("Ignoring requested conf " + args.conf + ": file not found.")

# READ CONFIG FILE
zones={} # a dictionary in which to place bgapp objects
thiszone = ""
zonesearch = "\[" + scriptname + ".*\]"
with open(conffile, "r") as infile:
   for line in infile:
      # remove comments and their preceding whitespace
      line = re.sub('\s*#.*$',"",line.rstrip('\n'))
      if debuglev(DEBUG_LINES_RAW): ferror("line \'" + line + "\'")
      zoneregex= re.compile(zonesearch)
      if zoneregex.match(line):
         # new zone
         thiszone = zoneregex.match(line).group(0).lstrip('[').rstrip(']').split(':')
         if len(thiszone) < 2:
            thiszone.append("default")
         if debuglev(DEBUG_LINES): ferror("Adding zone " + thiszone[1])
         zones[thiszone[1]] = localapp.bgapp(thiszone[1])
      else:
         if len(line) > 0:
            # i.e., this is not a blankline
            thisline = shlex.split(line)

            if thisline[0] == "force":
               zones[thiszone[1]].force = istruthy(thisline[1])
               if debuglev(DEBUG_LINES): ferror("Setting " + thiszone[1] + ".force = " + str(zones[thiszone[1]].force))

            elif thisline[0] == "overwrite":
               zones[thiszone[1]].overwrite = istruthy(thisline[1])
               if debuglev(DEBUG_LINES): ferror("Setting " + thiszone[1] + ".overwrite = " + str(zones[thiszone[1]].force))

            elif thisline[0] == "check":
               zones[thiszone[1]].check = thisline[1]
               if debuglev(DEBUG_LINES): ferror("Setting " + thiszone[1] + ".check = " + str(zones[thiszone[1]].check))

            elif thisline[0] == "file":
               zones[thiszone[1]].files.append(localapp.bgfile(thisline[1],thisline[2]))
               if debuglev(DEBUG_LINES): ferror("Adding " + thiszone[1] + " file source = " + thisline[1] + " dest = " + thisline[2])

            elif thisline[0] == "directory" or thisline[0] == "dir":
               zones[thiszone[1]].directories.append(localapp.bgdirectory(thisline[1],thisline[2]))
               if debuglev(DEBUG_LINES): ferror("Adding " + thiszone[1] + " dir source = " + thisline[1] + " dest = " + thisline[2])

            elif thisline[0] == "action":
               #zones[thiszone[1]].action = line.lstrip("action").lstrip()
               zones[thiszone[1]].action = thisline[1]
               if debuglev(DEBUG_LINES): ferror("Setting " + thiszone[1] + " action = \'" + zones[thiszone[1]].action + "\'")

            elif thisline[0] == "source":
               zones[thiszone[1]].source = thisline[1]
               if debuglev(DEBUG_LINES): ferror("Setting " + thiszone[1] + " source = " + zones[thiszone[1]].source)

            elif thiszone[1] == "default":
               if thisline[0] == "forceall":
                  forceall = istruthy(thisline[1])
                  zones[thiszone[1]].forceall = forceall
                  if debuglev(DEBUG_LINES): ferror("Setting forceall = " + str(forceall))
               if thisline[0] == "overwriteall":
                  overwriteall = istruthy(thisline[1])
                  zones[thiszone[1]].overwriteall = overwriteall
                  if debuglev(DEBUG_LINES): ferror("Setting overwriteall = " + str(overwriteall))
               elif thisline[0] == "minversion":
                  _scriptversion = ''.join([i for i in bgconfpyversion if i.isdigit()])
                  _conffileversion = ''.join([i for i in thisline[1] if i.isdigit()])
                  if _conffileversion > _scriptversion:
                     ferror("Config file " + conffile + " is newer version: " + thisline[1] + ". Aborted.")
                     sys.exit(6)
                  elif debuglev(DEBUG_LINES): ferror("Validated conffile version " + thisline[1])
            else:
               ferror("Ignoring unknown: \'" + line + "\'")

# APPLY COMMAND_LINE ARGUMENTS
# apply after config file, because cli always trumps config
# 1. Load default values into local variables
if args.dry is not None: dryrun = args.dry
if dryrun and debuglev(1):
   ferror("DRY RUN ONLY")
elif debuglev(DEBUG_EXECUTE):
   ferror("EXECUTION PHASE")
if debuglev(DEBUG_OPTIONS):
   ferror("Default: overwriteall:", overwriteall, "\tforceall:", forceall)

# PERFORM DEPLOYMENTS
# 2. Execute regular applications
_needaction=False
for thisname, thisapp in zones.items():
   if not thisname == "default":
      # check for existence of application
      if thisapp.check is None or thisapp.check == "" or os.path.isfile(thisapp.check) or forceall or thisapp.force:
         if debuglev(2): ferror("Applying " + thisname + ": overwrite:", thisapp.overwrite, "\tforce:", thisapp.force)
         for thisfile in thisapp.files:
            copyifactive("file", thisfile.source, thisfile.dest, thisapp)
         for thisdir in thisapp.directories:
            copyifactive("dir", thisdir.source, thisdir.dest, thisapp)
         if thisapp.action != "":
            act(thisapp.action, thisapp)
      else:
         if debuglev(2): ferror("Skipping " + thisname)

# 3. Execute default zone last
defaultzone = zones["default"]
if debuglev(2): ferror("Default:")
for thisfile in defaultzone.files:
   copyifactive("file", thisfile.source, thisfile.dest, defaultzone)
for thisdir in zones["default"].directories:
   copyifactive("dir", thisdir.source, thisdir.dest, defaultzone)
if zones["default"].action != "":
   act(zones["default"].action, zones["default"])
if dryrun and debuglev(1): ferror("DRY RUN ONLY")
