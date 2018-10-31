#include <cstddef>

#define CHUNKSIZE 0x100000
#define MAXRETRIES 5

class Buffer {
public:
    int fd;
    char* chunk;
    size_t got;
    size_t offset;
    size_t prev_offset;
    unsigned nevents;
    unsigned long timestamp;
    size_t block_offset;
    size_t block_size;
    
    Buffer(int fd);
    ~Buffer();
    void reset_buffer();
    void print_got();
    size_t read_with_retries(size_t displacement, size_t count);
    void read_partial();
};

