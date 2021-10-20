from psana.psexp import DataSourceBase
from psana.dgrmdsource import DgrmDsource

class DrpDataSource(DataSourceBase):

    def __init__(self, *args, **kwargs):
        super(DrpDataSource, self).__init__(**kwargs)
        self.runnum_list = [0] 
        self.runnum_list_index = 0
        self._setup_run()
        super(). _start_prometheus_client()

    def __del__(self):
        super(). _end_prometheus_client()
    
    def runs(self):
        yield 0
    
    def is_mpi(self):
        return False
    
    def _setup_run(self):
        if self.runnum_list_index == len(self.runnum_list):
            return False
        
        runnum = self.runnum_list[self.runnum_list_index]
        self.dgds = DgrmDsource()
        
        # Both SingleFile and Shmem DataSource
        self.dm = DgramManager(['shmem'], tag=self.tag)
        
        self._configs = self.dm.configs
        super()._setup_det_class_table()
        super()._set_configinfo()
        self.runnum_list_index += 1
        return True
