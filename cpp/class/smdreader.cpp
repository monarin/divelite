#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <vector>
#include <memory>

#include "smdreader.h"
using namespace std;

/* Xtc remanufactored struct for simple data acess and the Buffer struct */
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

SmdReader::SmdReader(vector<int> _fds) {
    fds = _fds;
    nfiles = fds.size();
    got_events = 0;
    limit_ts = 1;
    dgram_size = sizeof(Dgram);
    xtc_size = sizeof(Xtc);
}

SmdReader::~SmdReader() {
    bufs.clear();
}

void SmdReader::get(unsigned nevents) {
    if (bufs.empty() == true) {
        for (auto i=fds.begin(); i != fds.end(); ++i) {
            cout << "creating buffer with fd=" << *i << endl;
            unique_ptr<Buffer> buf(new Buffer{*i});
            cout << buf.get() << endl;
            bufs.push_back(move(buf));
            cout << bufs[bufs.size()-1].get() << endl;
            cout << buf.get() << endl;
        }
    }
}

