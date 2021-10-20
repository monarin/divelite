from psana       import dgram
from psana.event import Event
from psana.psexp import PacketFooter, TransitionId, PrometheusManager
import numpy as np
import os
import time

import logging
logger = logging.getLogger(__name__)

s_bd_just_read = PrometheusManager.get_metric('psana_bd_just_read')
s_bd_gen_smd_batch = PrometheusManager.get_metric('psana_bd_gen_smd_batch')
s_bd_gen_evt = PrometheusManager.get_metric('psana_bd_gen_evt')

class EventManager(object):
    """ Return an event from the received smalldata memoryview (view)

    1) If dm is empty (no bigdata), yield this smd event
    2) If dm is not empty, 
        - with filter fn, fetch one bigdata and yield it.
        - w/o filter fn, fetch one big chunk of bigdata and
          replace smalldata view with the read out bigdata.
          Yield one bigdata event.
    """
    def __init__(self, view, smd_configs, dm, esm, 
            filter_fn=0, prometheus_counter=None, 
            max_retries=0, use_smds=[]):
        if view:
            pf = PacketFooter(view=view)
            self.n_events = pf.n_packets
        else:
            self.n_events = 0

        self.smd_configs = smd_configs
        self.dm = dm
        self.esm = esm
        self.n_smd_files = len(self.smd_configs)
        self.filter_fn = filter_fn
        self.prometheus_counter = prometheus_counter
        self.max_retries = max_retries
        self.use_smds = use_smds
        self.smd_view = view
        self.i_evt = 0

        # Each chunk must fit in BD_CHUNKSIZE and we only fill bd buffers
        # when bd_offset reaches the size of buffer.
        self.BD_CHUNKSIZE = int(os.environ.get('PS_BD_CHUNKSIZE', 0x1000000))
        self._get_offset_and_size()
        if self.dm.n_files > 0:
            self._init_bd_chunks()

    def __iter__(self):
        return self

    def _inc_prometheus_counter(self, unit, value=1):
        if self.prometheus_counter:
            self.prometheus_counter.labels(unit,'None').inc(value)

    @s_bd_gen_evt.time()
    def __next__(self):
        if self.i_evt == self.n_events: 
            raise StopIteration
        
        evt = self._get_next_evt()
        
        # Update EnvStore - this is the earliest we know if this event is a Transition
        # make sure we update the envstore now rather than later.
        if evt.service() != TransitionId.L1Accept:
            self.esm.update_by_event(evt)
        
        return evt
    
    def _get_bd_offset_and_size(self, d, current_bd_offsets, current_bd_chunk_sizes, i_evt, i_smd, i_first_L1):
        if self.use_smds[i_smd]: return

        # Get offset and size of bd buffer
        # For transitions, this is the current bd offset
        if hasattr(d, "smdinfo"):
            self.bd_offset_array[i_evt, i_smd] = d.smdinfo[0].offsetAlg.intOffset
            self.bd_size_array[i_evt, i_smd] = d.smdinfo[0].offsetAlg.intDgramSize 
        else:
            self.bd_offset_array[i_evt, i_smd] = current_bd_offsets[i_smd]
            self.bd_size_array[i_evt, i_smd] = d._size
        
        # Check continuous chunk 
        if current_bd_chunk_sizes[i_smd] + self.bd_size_array[i_evt, i_smd] < self.BD_CHUNKSIZE:
            if i_evt > i_first_L1 and \
                    current_bd_offsets[i_smd] == self.bd_offset_array[i_evt, i_smd]:
                self.cutoff_flag_array[i_evt, i_smd] = 0
                current_bd_chunk_sizes[i_smd] += self.bd_size_array[i_evt, i_smd]

        if self.cutoff_flag_array[i_evt, i_smd] == 1:
            current_bd_chunk_sizes[i_smd] = self.bd_size_array[i_evt, i_smd]

        """
        if current_bd_offsets[i_smd] == self.bd_offset_array[i_evt, i_smd]  \
                and i_evt != i_first_L1                                     \
                and current_bd_chunk_sizes[i_smd] + self.bd_size_array[i_evt, i_smd] < self.BD_CHUNKSIZE:
            self.cutoff_flag_array[i_evt, i_smd] = 0
            current_bd_chunk_sizes[i_smd] += self.bd_size_array[i_evt, i_smd]
        else:
            current_bd_chunk_sizes[i_smd] = self.bd_size_array[i_evt, i_smd]
        """
        current_bd_offsets[i_smd] = self.bd_offset_array[i_evt, i_smd] + self.bd_size_array[i_evt, i_smd]
        print(f'i_smd:{i_smd} i_evt:{i_evt} i_first_L1:{i_first_L1} current_bd_chunk_size={current_bd_chunk_sizes[i_smd]} current_bd_offset:{current_bd_offsets[i_smd]} bd_offset:{self.bd_offset_array[i_evt, i_smd]} bd_size:{self.bd_size_array[i_evt, i_smd]}')
        
    @s_bd_gen_smd_batch.time()
    def _get_offset_and_size(self):
        """
        Use fast step-through to read off offset and size from smd_view.
        Format of smd_view 
        [
          [[d_bytes][d_bytes]....[evt_footer]] <-- 1 event 
          [[d_bytes][d_bytes]....[evt_footer]]
          [chunk_footer]]
        """
        offset = 0
        i_smd = 0
        smd_chunk_pf = PacketFooter(view=self.smd_view)
        dtype = np.int64
        # Row - events, col = smd files
        self.bd_offset_array    = np.zeros((smd_chunk_pf.n_packets, self.n_smd_files), dtype=dtype) 
        self.bd_size_array      = np.zeros((smd_chunk_pf.n_packets, self.n_smd_files), dtype=dtype)
        self.smd_offset_array   = np.zeros((smd_chunk_pf.n_packets, self.n_smd_files), dtype=dtype)
        self.smd_size_array     = np.zeros((smd_chunk_pf.n_packets, self.n_smd_files), dtype=dtype)
        self.new_chunk_id_array = np.zeros((smd_chunk_pf.n_packets, self.n_smd_files), dtype=dtype)
        self.cutoff_flag_array  = np.ones((smd_chunk_pf.n_packets, self.n_smd_files), dtype=dtype)
        self.services           = np.zeros(smd_chunk_pf.n_packets, dtype=dtype)
        smd_aux_sizes           = np.zeros(self.n_smd_files, dtype=dtype)
        self.i_first_L1s        = np.zeros(self.n_smd_files, dtype=dtype) + 0xffffff
        # For comparing if the next dgram should be in the same read
        current_bd_offsets      = np.zeros(self.n_smd_files, dtype=dtype) 
        # Current chunk size (gets reset at boundary)
        current_bd_chunk_sizes  = np.zeros(self.n_smd_files, dtype=dtype) 
        i_evt = 0
        while offset < memoryview(self.smd_view).nbytes - memoryview(smd_chunk_pf.footer).nbytes:
            if i_smd == 0:
                smd_evt_size = smd_chunk_pf.get_size(i_evt)
                smd_evt_pf = PacketFooter(view=self.smd_view[offset: offset+smd_evt_size])
                smd_aux_sizes[:] = [smd_evt_pf.get_size(i) for i in range(smd_evt_pf.n_packets)]

            # Only get offset and size of non-missing dgram
            # TODO: further optimization by looking for the first L1 and read in a big chunk
            # anything that comes after. Right now, all transitions mark the cutoff points.
            if smd_aux_sizes[i_smd] == 0:
                self.cutoff_flag_array[i_evt, i_smd] = 0
            else:
                d = dgram.Dgram(config=self.smd_configs[i_smd], view=self.smd_view, offset=offset)
                
                self.smd_offset_array[i_evt, i_smd] = offset
                self.smd_size_array[i_evt, i_smd]   = d._size
                self.services[i_evt] = d.service()

                # Any dgrams after the first L1 (as long as they fit in the chunk size)
                # will be read in together. 
                if self.dm.n_files > 0:
                    if d.service() == TransitionId.L1Accept:
                        if self.i_first_L1s[i_smd] == 0xffffff: 
                            self.i_first_L1s[i_smd] = i_evt
                            print(f'i_smd={i_smd} i_first_L1={self.i_first_L1s[i_smd]}')

                    # For SlowUpdate, we need to check if the next dgram gets cutoff
                    elif d.service() == TransitionId.SlowUpdate and hasattr(d, 'chunkinfo'):
                        stream_id = self.dm.get_stream_id(i_smd)
                        _chunk_ids = [getattr(d.chunkinfo[seg_id].chunkinfo, 'chunkid') for seg_id in d.chunkinfo]
                        # There must be only one unique epics var
                        if _chunk_ids: self.new_chunk_id_array[i_evt, i_smd] = _chunk_ids[0] 
                    
                    self._get_bd_offset_and_size(d, current_bd_offsets, current_bd_chunk_sizes, 
                            i_evt, i_smd, self.i_first_L1s[i_smd])

                """
                # For L1 with bigdata files, store offset and size found in smd dgrams.
                # For SlowUpdate, store new chunk id (if found). TODO: check if
                # we need to always check for epics for SlowUpdate.
                if d.service() == TransitionId.L1Accept and self.dm.n_files > 0:
                    if i_first_L1 == -1:
                        i_first_L1 = i_evt
                        print(f'i_smd={i_smd} i_first_L1={i_first_L1}')
                    self._get_bd_offset_and_size(d, current_bd_offsets, current_bd_chunk_sizes, i_evt, i_smd, i_first_L1)
                elif d.service() == TransitionId.SlowUpdate and hasattr(d, 'chunkinfo'):
                    # We only support chunking on bigdata
                    if self.dm.n_files > 0: 
                        stream_id = self.dm.get_stream_id(i_smd)
                        _chunk_ids = [getattr(d.chunkinfo[seg_id].chunkinfo, 'chunkid') for seg_id in d.chunkinfo]
                        # There must be only one unique epics var
                        if _chunk_ids: self.new_chunk_id_array[i_evt, i_smd] = _chunk_ids[0] 
                """
            
            offset += smd_aux_sizes[i_smd]            
            i_smd += 1
            if i_smd == self.n_smd_files: 
                offset += PacketFooter.n_bytes * (self.n_smd_files + 1) # skip the footer
                i_smd = 0  # reset to the first smd file
                i_evt += 1 # done with this smd event
        
        # end while offset

        # Precalculate cutoff indices
        self.cutoff_indices = []
        self.chunk_indices  = np.zeros(self.n_smd_files, dtype=dtype)
        for i_smd in range(self.n_smd_files):
            self.cutoff_indices.append(np.where(self.cutoff_flag_array[:, i_smd] == 1)[0])
            print(f'i_smd={i_smd} cutoff_index={self.cutoff_indices[i_smd]} services={self.services[self.cutoff_indices[i_smd]]}')

    def _open_new_bd_file(self, i_smd, new_chunk_id):
        os.close(self.dm.fds[i_smd])
        xtc_dir = os.path.dirname(self.dm.xtc_files[i_smd])
        filename = os.path.basename(self.dm.xtc_files[i_smd])
        found = filename.find('-c')
        new_filename = filename.replace(filename[found:found+4], '-c'+str(new_chunk_id).zfill(2))
        fd = os.open(os.path.join(xtc_dir, new_filename), os.O_RDONLY)
        self.dm.fds[i_smd] = fd
        self.dm.xtc_files[i_smd] = new_filename
    
    @s_bd_just_read.time()
    def _read(self, fd, size, offset):
        st = time.monotonic()
        chunk = bytearray()
        for i_retry in range(self.max_retries+1):
            chunk.extend(os.pread(fd, size, offset))
            got = memoryview(chunk).nbytes
            if got == size:
                break
            offset += got
            size -= got

            found_xtc2_flags = self.dm.found_xtc2('bd')
            if got == 0 and all(found_xtc2_flags):
                print(f'bigddata got 0 byte and .xtc2 files found on disk. stop reading this .inprogress file')
                break

            print(f'bigdata read retry#{i_retry} - waiting for {size/1e6} MB, max_retries: {self.max_retries} (PS_R_MAX_RETRIES), sleeping 1 second...') 
            time.sleep(1)
        
        en = time.monotonic()
        sum_read_nbytes = memoryview(chunk).nbytes # for prometheus counter
        rate = 0
        if sum_read_nbytes > 0:
            rate = (sum_read_nbytes/1e6)/(en-st)
        logger.debug(f"bd reads chunk {sum_read_nbytes/1e6:.5f} MB took {en-st:.2f} s (Rate: {rate:.2f} MB/s)")
        self._inc_prometheus_counter('MB', sum_read_nbytes/1e6)
        self._inc_prometheus_counter('seconds', en-st)
        return chunk

    def _init_bd_chunks(self):
        self.bd_bufs = [bytearray() for i in range(self.n_smd_files)]
        self.bd_buf_offsets = np.zeros(self.n_smd_files, dtype=np.int64)
    
    def _fill_bd_chunk(self, i_smd):
        """
        Fill self.bigdatas for this given stream id 
        No filling: No bigdata files or 
           when this stream doesn't have at least a dgram. 
        Detail:
            - Ignore all transitions
            - Read the next chunk
              From cutoff_flag_array[:, i_smd], we get cutoff_indices as
              [0, 1, 2, 12, 13, 18, 19] a list of index to where each read 
              or copy will happen. 
        """
        # Check no filling
        if self.use_smds[i_smd]: return
        
        # Reset buffer offset with new filling
        self.bd_buf_offsets[i_smd] = 0

        cutoff_indices = self.cutoff_indices[i_smd]
        i_evt_cutoff = cutoff_indices[self.chunk_indices[i_smd]]
        begin_chunk_offset = self.bd_offset_array[i_evt_cutoff, i_smd]

        # Calculate read size:
        # For last chunk, read size is the sum of all bd dgrams all the
        # way to the end of the array. Otherwise, only sum to the next chunk.
        if self.chunk_indices[i_smd] == cutoff_indices.shape[0] - 1:
            read_size = np.sum(self.bd_size_array[i_evt_cutoff:, i_smd])
        else:
            i_next_evt_cutoff = cutoff_indices[self.chunk_indices[i_smd] + 1]
            read_size = np.sum(self.bd_size_array[i_evt_cutoff:i_next_evt_cutoff, i_smd])
        self.bd_bufs[i_smd] = self._read(self.dm.fds[i_smd], read_size, begin_chunk_offset)

    def _get_next_evt(self):
        """ Generate bd evt for different cases:
        1) No bigdata or is a Transition Event prior to i_first_L1
            create dgrams from smd_view
        2) L1Accept event
            create dgrams from bd_bufs
        3) L1Accept with some smd files replaced by bigdata files
            create dgram from smd_view if use_smds[i_smd] is set
            otherwise create dgram from bd_bufs
        """
        dgrams = [None] * self.n_smd_files
        for i_smd in range(self.n_smd_files):
            # Check in case we need to switch to the next bigdata chunk file
            if self.services[self.i_evt] != TransitionId.L1Accept:
                if self.new_chunk_id_array[self.i_evt, i_smd] != 0:
                    print(f'open_new_bd_file i_smd={i_smd} chunk_id={self.new_chunk_id_array[self.i_evt, i_smd]}')
                    self._open_new_bd_file(i_smd, 
                            self.new_chunk_id_array[self.i_evt, i_smd])
                
            view, offset, size = (bytearray(),0,0)
            # Try to create dgram from smd view
            if self.dm.n_files == 0 or self.use_smds[i_smd] \
                    or self.i_evt < self.i_first_L1s[i_smd]:
                view = self.smd_view
                offset = self.smd_offset_array[self.i_evt, i_smd]
                size = self.smd_size_array[self.i_evt, i_smd]

                # Non L1 dgram prior to i_first_L1 are counted as a new "chunk" 
                # because their cutoff flag is set (data coming from smd view 
                # instead of bd chunk). We'll need to update chunk index for
                # this smd when we see non L1.
                self.chunk_indices[i_smd] += 1

            else:
                # Check if we need to fill bd buf if this dgram doesn't fit in the current view
                if self.bd_buf_offsets[i_smd] + self.bd_size_array[self.i_evt, i_smd] \
                        > memoryview(self.bd_bufs[i_smd]).nbytes:
                    self._fill_bd_chunk(i_smd)
                    self.chunk_indices[i_smd] += 1
                
                # This is the offset of bd buffer! and not what stored in smd dgram,
                # which in contrast points to the location of disk.
                offset = self.bd_buf_offsets[i_smd] 
                size = self.bd_size_array[self.i_evt, i_smd] 
                view = self.bd_bufs[i_smd]
                self.bd_buf_offsets[i_smd] += size
            
            if size:  # handles missing dgram
                dgrams[i_smd] = dgram.Dgram(config=self.dm.configs[i_smd], view=view, offset=offset)

        self.i_evt += 1
        self._inc_prometheus_counter('evts')
        evt = Event(dgrams=dgrams, run=self.dm.get_run()) 
        print(f'YIELD ts={evt.timestamp} service={evt.service()}')
        return evt


