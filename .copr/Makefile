srpm:
	dnf -y install git rpmdevtools
	rpmdev-setuptree
	export SRCDIR=$$(rpm --eval "%{_sourcedir}") && \
	./get-sources.sh $(spec) && \
	cp -v *.patch $${SRCDIR}
	rpmbuild -bs $(spec)
	SRPMDIR=$$(rpm --eval "%{_srcrpmdir}") && \
	mv -v $${SRPMDIR}/* $(outdir)
