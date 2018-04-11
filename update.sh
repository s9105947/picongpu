#!/bin/bash
#
# update the doxygen docu with branch in $1

branch=${1:-"dev"}
myDir=`pwd`

# tmp dir with auto-delete if something goes wrong
TMPDIR=`mktemp -d`
trap "{ cd - ; rm -rf $TMPDIR; exit 255; }" SIGINT

# create new documentation
cd $TMPDIR
git clone https://github.com/ComputationalRadiationPhysics/picongpu.git
cd picongpu
git checkout $branch
cd docs
sed -i 's/GENERATE_HTML.*=.*NO/GENERATE_HTML     = YES/' Doxyfile
sed -i 's/GENERATE_XML.*=.*YES/GENERATE_XML      = NO/' Doxyfile
doxygen

# update old documentation
cd $myDir
rsync -r --delete --filter='P update.sh' --filter='P .git' --filter="P .nojekyll" $TMPDIR/picongpu/docs/html/ .

rm -rf $TDIR
exit 0
