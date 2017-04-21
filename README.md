### Overview
bgconf is my personal collection of conf files.
For the description of the package itself, view usr/share/bgconf/docs/README.txt.

### Building
The recommended way to build an rpm is:

    pushd ~/rpmbuild; mkdir -p SOURCES RPMS SPECS BUILD BUILDROOT; popd
    mkdir -p ~/rpmbuild/SOURCES/bgconf-0.1-1/
    cd ~/rpmbuild/SOURCES/bgconf-0.1-1
    git clone https://github.com/bgstack15/bgconf
    usr/share/bgconf/inc/pack rpm

The generated rpm will be in ~/rpmbuild/RPMS/noarch

### NOTES
This is for internal use and should not be published to the Internet.
