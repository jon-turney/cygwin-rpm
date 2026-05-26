#!
SPEC=${1:-cygwin.spec}
SRCDIR=${SRCDIR:-.}
REF=$(echo %git_ref | rpmspec -q --shell --srpm ${SPEC} 2>/dev/null | tail -2 | head -1)
git archive --prefix newlib-cygwin/ --output ${SRCDIR}/newlib-cygwin-${REF}.tar.bz2 --remote git://cygwin.com/git/newlib-cygwin ${REF}
