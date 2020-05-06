#./configure --prefix=$PREFIX 
./configure --prefix=$PREFIX --with-lsf=/afs/slac/package/lsf/curr/ --with-lsf-libdir=/afs/slac/package/lsf/curr/lib/ --enable-mpi-cxx --with-verbs
make -j $CPU_COUNT
make install
