#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

#include "buffer.h"

using namespace std;

Buffer::Buffer(int _fd) {
    fd = _fd;
    chunk = (char *)malloc(CHUNKSIZE);
    cout << "create chunk " << &chunk << endl;
    got = read_with_retries(0, CHUNKSIZE);
    offset = 0;
    prev_offset = 0;
    nevents = 0;
    timestamp = 0;
    block_offset = 0;
    block_size = 0;
}

Buffer::~Buffer() {
    cout << "destroy chunk " << &chunk << endl;
    free(chunk);
}

void Buffer::reset_buffer() {
    nevents = 0;
    block_size = 0;
    block_offset = offset;
}

void Buffer::print_got() {
    cout << "got " << got << endl;
}

size_t Buffer::read_with_retries(size_t displacement, size_t count) {
    char* tmp_chunk = chunk + displacement;
    size_t requested = count;
    size_t tmp_got = 0;
    for (int attempt=0; attempt<MAXRETRIES; attempt++) {
        tmp_got = read(fd, tmp_chunk, count);
        if (tmp_got == count) {
            return requested;
        } else {
            tmp_chunk += tmp_got;
            count -= tmp_got;
        }
    return requested - count;
    }
}

void Buffer::read_partial(size_t _block_offset, size_t _dgram_offset) {
    // Reads partial chunk
    // First copy what remains in the chunk to the beginning of
    // the chunk then re-read to fill in the chunk.
    char* tmp_chunk = chunk;
    size_t remaining = CHUNKSIZE - _block_offset;
    if (remaining > 0) {
        memcpy(tmp_chunk, tmp_chunk + _block_offset, remaining);
    }

    size_t new_got = Buffer::read_with_retries(remaining, CHUNKSIZE - remaining);
    if (new_got == 0) {
        got = 0; // nothing more to read
    } else {
        got = remaining + new_got;
    }
    offset = _dgram_offset - _block_offset;
}
