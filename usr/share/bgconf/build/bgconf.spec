Summary:	set of confs for standard deployments
Name:		bgconf
Version:	0.1
Release:	14
License:	CC BY-SA 4.0
Group:		Applications/System
Source:		bgconf.tgz
URL:		https://bgstack15.wordpress.com/
#Distribution:
#Vendor:
Packager:	B Stack <bgstack15@gmail.com>
Buildarch:	noarch
Requires(pre):	/usr/bin/python3

%global _python_bytecompile_errors_terminate_build 0

%description
Bgconf includes configs for standard applications in my PC deployments.
A special python script deploys the confs based on its own config file and the presence of the specified applications. See file /usr/share/bgconf/bgconf.conf.

%prep
%setup

%build

%install
rm -rf %{buildroot}
rsync -a . %{buildroot}/ --exclude='**/.*.swp' --exclude='**/.git' --exclude='**/__pycache__'

%clean
rm -rf %{buildroot}

%post
# rpm post 2017-10-14
# nothing to do here because the rpm can include the symlink for /usr/share/doc/bgconf
exit 0

%preun
# rpm preun 2017-10-14
rm -rf /usr/share/bgconf/__pycache__ /usr/share/bgconf/*.pyc 2>/dev/null ||:
exit 0

%postun

%files
%dir /usr/share/bgconf
%dir /usr/share/bgconf/confs-example
%dir /usr/share/bgconf/inc
%dir /usr/share/bgconf/build
%dir /usr/share/bgconf/build/debian-bgconf
%dir /usr/share/bgconf/confs
/usr/share/bgconf/bgconf.py
/usr/share/bgconf/bgconf.pyc
/usr/share/bgconf/bgconf.pyo
/usr/share/bgconf/doc
%config %attr(666, -, -) /usr/share/bgconf/bgconf.conf
%config %attr(666, -, -) /usr/share/bgconf/bgconf.conf-example
/usr/share/bgconf/inc/dconf.sh
/usr/share/bgconf/inc/xfce.sh
/usr/share/bgconf/inc/xfconf.sh
%doc %attr(444, -, -) /usr/share/bgconf/build/confs.txt
/usr/share/bgconf/build/get-files
/usr/share/bgconf/build/pack
/usr/share/bgconf/build/bgconf.spec
%doc %attr(444, -, -) /usr/share/bgconf/build/files-for-versioning.txt
/usr/share/bgconf/build/debian-bgconf/compat
/usr/share/bgconf/build/debian-bgconf/md5sums
/usr/share/bgconf/build/debian-bgconf/preinst
/usr/share/bgconf/build/debian-bgconf/prerm
/usr/share/bgconf/build/debian-bgconf/control
/usr/share/bgconf/build/debian-bgconf/postrm
/usr/share/bgconf/build/debian-bgconf/conffiles
/usr/share/bgconf/build/debian-bgconf/postinst
/usr/share/bgconf/build/debian-bgconf/changelog
/usr/share/bgconf/localapp.py
/usr/share/bgconf/localapp.pyc
/usr/share/bgconf/localapp.pyo
%doc %attr(444, -, -) /usr/share/doc/bgconf/README.txt
%doc %attr(444, -, -) /usr/share/doc/bgconf/version.txt
%dir /usr/share/bgconf/confs/irfan
%attr(666, -, -) /usr/share/bgconf/confs/irfan/i_view32.ini
%dir /usr/share/bgconf/confs/firefox
/usr/share/bgconf/confs/firefox/*
%dir /usr/share/bgconf/confs/scite
%attr(666, -, -) /usr/share/bgconf/confs/scite/SciTEGlobal.properties
%dir /usr/share/bgconf/confs/fstab
/usr/share/bgconf/confs/fstab/*
%attr(600, root, root) /usr/share/bgconf/confs/fstab/.bgirton.smith122.com
%ghost /usr/share/bgconf/__pycache__
%ghost /usr/share/bgconf/__pycache__/localapp.cpython-35.pyc
%dir /usr/share/bgconf/confs/vlc
/usr/share/bgconf/confs/vlc/*
%dir /usr/share/bgconf/confs/plank
/usr/share/bgconf/confs/plank/*
%dir /usr/share/bgconf/confs/puddletag
/usr/share/bgconf/confs/puddletag/*
/usr/share/bgconf/confs/xscreensaver
/usr/share/bgconf/confs/cinnamon
/usr/share/bgconf/confs/xfce
/usr/share/bgconf/confs/vim
/usr/share/bgconf/confs/desktop-theme
/usr/share/bgconf/confs/git
/usr/share/bgconf/confs/ott
/usr/share/bgconf/confs/ssh
/usr/share/bgconf/confs/dash
/usr/share/bgconf/confs/bc
/usr/share/bgconf/confs/copyq
/usr/share/bgconf/confs/display-manager

%changelog
* Sun Jan 28 2017 B Stack <bgstack15@gmail.com> 0.1-14
- Updated content. See doc/README.txt.

* Sun Dec 10 2017 B Stack <bgstack15@gmail.com> 0.1-13
- Updated content. See doc/README.txt.

* Sun Nov 19 2017 B Stack <bgstack15@gmail.com> 0.1-12
- Updated content. See doc/README.txt.

* Sat Oct 14 2017 B Stack <bgstack15@gmail.com> 0.1-11
- Updated content. See doc/README.txt.

* Sun Sep 17 2017 B Stack <bgstack15@gmail.com> 0.1-10
- Updated content. See doc/README.txt.

* Sun Apr  9 2017 B Stack <bgstack15@gmail.com> 0.1-1
- Initial rpm build
