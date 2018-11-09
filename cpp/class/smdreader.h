#include <vector>
#include <memory>

#include "buffer.h"

/* Xtc remanufactored struct for simple data acess*/
struct Xtc {
    int junks[4];
    unsigned extent;
};

struct Sequence {
    int junks[2];
    unsigned low;
    unsigned high;
};

struct Dgram {
    Sequence seq;
    int junks[4];
    Xtc xtc;
};

class SmdReader {
public:
    std::vector<int> fds;
    std::vector<std::shared_ptr<Buffer>> bufs;
    int nfiles;
    unsigned got_events;
    unsigned long limit_ts;
    size_t dgram_size;
    size_t xtc_size;
    double dt_get_init, dt_get_dgram, dt_reread;
    
    SmdReader(std::vector<int> _fds);
    ~SmdReader();
    int check_reread(std::shared_ptr<Buffer> *buf_ptr_ptr);
    //size_t get_payload(std::shared_ptr<Buffer> *buf_ptr, Dgram** d_ptr_ptr);
    //void get_dgram(std::shared_ptr<Buffer> *buf_ptr, Dgram** d_ptr_ptr, size_t payload);
    void get(unsigned nevents);

};
