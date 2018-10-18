from psana import DataSource

#ds = DataSource('exp=xpptut15:run=1')
#ds.print_type()

ds = DataSource('/reg/neh/home/monarin/lcls2/psana/psana/tests/data.xtc')
#shmem_ds.print_type()
for nevent, evt in enumerate(ds.events()):
    print(nevent)

