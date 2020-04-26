Building and uploading openmpi and mpi4py to local channel  
cd openmpi  
conda build . 
cd ../mpi4py
conda build .

Create and index local channel
CHANNEL_DIR=~/conda_channels/channel/linux-64
mkdir -p $CHANNEL_DIR
cd $CHANNEL_DIR
ln -s /reg/neh/home/monarin/miniconda3/conda-bld/linux-64/openmpi-4.0.0-3.tar.bz2 openmpi-4.0.0-3.tar.bz2
ln -s /reg/neh/home/monarin/miniconda3/conda-bld/linux-64/mpi4py-3.0.1a0-py37_34.tar.bz2 mpi4py-3.0.1a0-py37_34.tar.bz2
cd ../../
conda index channel

Test on new env
conda create -n test
conda activate test
conda install mpi4py -c file:///reg/neh/home/monarin/conda_channels/channel/
* check that both mpi4py and openmpi comes from the local channel 


 
