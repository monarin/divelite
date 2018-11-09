#include <stdlib.h>

#include "dummy.h"
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

Dummy::Dummy(int _id) {
    id = _id;
    chunk = (char *)malloc(CHUNKSIZE);
}

Dummy::~Dummy() {
    free(chunk);
}

void Dummy::multiply(int factor) {
    id *= factor;
}

void Dummy::get(size_t offset) {
    for (int i=0; i<8000; ++i) {
        Dgram* d = (Dgram*)(chunk + offset); 
        offset += sizeof(Dgram);
    }
}

