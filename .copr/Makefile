srpm:
	pwd
	dnf -y install git rpmdevtools
	rpmdev-setuptree
	TAG=$$(grep 'Version:' $(spec) | tr -s ' ' | cut -d ' ' -f2) && \
	SRCDIR=$$(rpm --eval "%{_sourcedir}") && \
	git archive --prefix newlib-cygwin/ --output $${SRCDIR}/newlib-cygwin-$${TAG}.tar.bz2 --remote git://cygwin.com/git/newlib-cygwin cygwin-$${TAG} && \
	cp -v *.patch $${SRCDIR}
	rpmbuild -bs $(spec)
	SRPMDIR=$$(rpm --eval "%{_srcrpmdir}") && \
	mv $${SRPMDIR}/* $(outdir)
