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
    got = read_with_retries(0, CHUNKSIZE);
    offset = 0;
    prev_offset = 0;
    nevents = 0;
    timestamp = 0;
    block_offset = 0;
}

Buffer::~Buffer() {
    free(chunk);
}

void Buffer::reset_buffer() {
    nevents = 0;
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

void Buffer::read_partial() {
    // Reads partial chunk
    // First copy what remains in the chunk to the beginning of
    // the chunk then re-read to fill in the chunk.
    // **Note that when got = 0, memcpy will complain overlap.
    // **Thit is the last chunk - ignore for now.
    size_t remaining = CHUNKSIZE - block_offset;
    if (remaining > 0) {
        memcpy(chunk, chunk + block_offset, remaining);
    }

    size_t new_got = Buffer::read_with_retries(remaining, CHUNKSIZE - remaining);
    if (new_got == 0) {
        got = 0; // nothing more to read
    } else {
        got = remaining + new_got;
    }
    offset = prev_offset - block_offset;
    block_offset = 0;
}
