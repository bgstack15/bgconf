Summary:	set of confs for standard deployments
Name:		bgconf
Version:	0.1
Release:	6
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

%preun
# rpm preun 2017-05-31
rm -rf /usr/share/bgconf/__pycache__ /usr/share/bgconf/*.pyc 2>/dev/null ||:
exit 0

%postun

%files
%dir /usr/share/bgconf
%dir /usr/share/bgconf/inc
%dir /usr/share/bgconf/confs-example
%dir /usr/share/bgconf/confs
%dir /usr/share/bgconf/docs
%dir /usr/share/bgconf/docs/debian-bgconf
%config %attr(666, -, -) /usr/share/bgconf/bgconf.conf
/usr/share/bgconf/inc/pack
/usr/share/bgconf/inc/get-files
%doc %attr(444, -, -) /usr/share/bgconf/inc/confs.txt
/usr/share/bgconf/localapp.py
/usr/share/bgconf/localapp.pyc
/usr/share/bgconf/localapp.pyo
%config %attr(666, -, -) /usr/share/bgconf/bgconf.conf-example
/usr/share/bgconf/docs/debian-bgconf/control
/usr/share/bgconf/docs/debian-bgconf/prerm
/usr/share/bgconf/docs/debian-bgconf/postinst
/usr/share/bgconf/docs/debian-bgconf/preinst
/usr/share/bgconf/docs/debian-bgconf/conffiles
/usr/share/bgconf/docs/debian-bgconf/changelog
/usr/share/bgconf/docs/debian-bgconf/md5sums
/usr/share/bgconf/docs/debian-bgconf/postrm
/usr/share/bgconf/docs/debian-bgconf/compat
%doc %attr(444, -, -) /usr/share/bgconf/docs/files-for-versioning.txt
/usr/share/bgconf/docs/bgconf.spec
%doc %attr(444, -, -) /usr/share/bgconf/docs/bgconf-version.txt
%doc %attr(444, -, -) /usr/share/bgconf/docs/README.txt
/usr/share/bgconf/bgconf.py
/usr/share/bgconf/bgconf.pyc
/usr/share/bgconf/bgconf.pyo
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
/usr/share/bgconf/confs/git
/usr/share/bgconf/confs/ott
/usr/share/bgconf/confs/ssh

%changelog
* Sun Apr  9 2017 B Stack <bgstack15@gmail.com> 0.1-1
- Initial rpm build
