This new event_manager.py tries to read bigdata in a bigger chunk.  
This is done by any location first L1Accept and anything that come
after including transitions (as long as they fit in BD_CHUNKSIZE)
will be read in together.

