File: /usr/share/bgconf/docs/README.txt
Package: bgconf
Author: bgstack15
Startdate: 2017-04-09
Title: Readme file for bgconf
Purpose: All packages should come with a readme
Usage: Read it.
Reference: README.txt
Improve:
Document: Below this line

### WELCOME
Bgconf includes my standard configs and a python script that deploys them.
The confs are provided in /usr/share/bgconf/confs/ and the definitions are in /usr/share/bgconf/bgconf.conf
After installation of the rpm, execute as the preferred user:
sudo /usr/share/bgconf/bgconf.py

### NOTES

### REFERENCE

### CHANGELOG

2017-04-09 B Stack <bgstack15@gmail.com> 0.1-1
- Wrote bgconf.conf

2017-04-22 B Stack <bgstack15@gmail.com> 0.1-2
- added vlc

2017-04-23 B Stack <bgstack15@gmail.com> 0.1-3
- Added xscreensaver
- Added puddletag
- Added plank not run on start
- Added bgstack15-red-k25 theme to ~/.themes directory
- Added cinnamon configs

2017-05-03 B Stack <bgstack15@gmail.com> 0.1-4
- Added git
- Added firefox extensions: password exporter, secure login (webextension), saved password editor

2017-05-28 B Stack <bgstack15@gmail.com> 0.1-5
- Added ott template file
- Updated fstab for Mersey network

2017-05-31 B Stack <bgstack15@gmail.com> 0.1-6
- Fixed the ./pack error where it makes a "cd" directory.
- Only runs dconf if it exists in cinnamon.
- Added GSSAPIDelegateCredentials yes to ssh_config.
- Added deb packaging.

2017-06-04 B Stack <bgstack15@gmail.com> 0.1-7
- Fixed the absence of the .git in the confs directory.

2017-06-12 B Stack <bgstack15@gmail.com> 0.1-8
- Added conf for dash fix
