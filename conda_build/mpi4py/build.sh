export PATH=/reg/common/package/openmpi/4.0.0-rhel6/bin:$PATH
which mpicc
$PYTHON setup.py install  --single-version-externally-managed --record=record.txt


mkdir -p $PREFIX/etc/conda/activate.d
mkdir -p $PREFIX/etc/conda/deactivate.d

ACTIVATE=$PREFIX/etc/conda/activate.d/openmpi.sh

# cpo - I believe we kept openmpi out of conda so we could support
# multiple OS-dependent versions at runtime like this.

# it's important that mpi4py only go into a local conda channel
# (not the cloud) since it is facility-specific

#echo 'rhel_version=$(less /etc/redhat-release | grep -o -E '[0-9]+' | head -1)' >> $ACTIVATE
#echo 'export PATH=/reg/common/package/openmpi/4.0.0-rhel$rhel_version/bin:$PATH' >> $ACTIVATE
#echo 'export LD_LIBRARY_PATH=/reg/common/package/openmpi/4.0.0-rhel$rhel_version/lib' >> $ACTIVATE

# version built on rhel7 that with LSF and verbs options
echo 'export LD_LIBRARY_PATH=/reg/common/package/openmpi/openmpi-4.0.2-verbs-lsf/install/lib' >> $ACTIVATE
echo 'export PATH=/reg/common/package/openmpi/openmpi-4.0.2-verbs-lsf/install/bin:$PATH' >> $ACTIVATE
