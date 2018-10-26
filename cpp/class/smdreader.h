#include <vector>
#include <memory>

#include "buffer.h"

class SmdReader {
public:
    std::vector<int> fds;
    std::vector<std::unique_ptr<Buffer>> bufs;
    int nfiles;
    unsigned got_events;
    unsigned long limit_ts;
    size_t dgram_size;
    size_t xtc_size;
    
    SmdReader(std::vector<int> _fds);
    ~SmdReader();
    void get(unsigned nevents);

};
