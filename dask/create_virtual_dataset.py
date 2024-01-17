from mpi4py import MPI
import sys
import h5py


in_f = h5py.File('/sdf/data/lcls/drpsrcf/ffb/users/monarin/h5/mylargeh5.h5', 'r')
n_files = 100


part_fnames = [f'/sdf/data/lcls/drpsrcf/ffb/users/monarin/h5/output/result_part{i}.h5' for i in range(n_files)]
part_files = [h5py.File(filename, 'r') for filename in part_fnames]


layouts = {}
for entry_key in in_f.keys():
    layouts[entry_key] = h5py.VirtualLayout(shape=in_f[entry_key].shape, dtype=in_f[entry_key].dtype)

with h5py.File('/sdf/data/lcls/drpsrcf/ffb/users/monarin/h5/output/result.h5', 'w', libver='latest') as out_f:
    for entry_key in in_f.keys():
        st,en = (0,0)
        print(f'Creating virtual source for {entry_key}')
        for i, filename in enumerate(part_fnames):
            vsource = h5py.VirtualSource(filename, entry_key, shape=part_files[i][entry_key].shape)
            en = st + part_files[i][entry_key].shape[0]
            print(f'  part{i} shape:{part_files[i][entry_key].shape} {st=} {en=}')
            layouts[entry_key][st:en] = vsource
            st = en 
        out_f.create_virtual_dataset(entry_key, layouts[entry_key], fillvalue=0)

# Close input h5 file
for i in range(n_files):
    part_files[i].close()
in_f.close()
