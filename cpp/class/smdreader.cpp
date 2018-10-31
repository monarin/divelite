#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <vector>
#include <memory>

#include "smdreader.h"
using namespace std;

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
            shared_ptr<Buffer> buf(new Buffer{*i});
            bufs.push_back(buf);
        }
    }

    got_events = 0;
    for (int i=0; i<bufs.size(); ++i) {
        bufs[i]->reset_buffer();
    }

    Dgram* d;
    size_t payload = 0;
    size_t remaining = 0;
    size_t dgram_offset = 0;
    int winner = 0;
    int needs_reread = 0;
    int i_st = 0;
    unsigned long current_max_ts = 0;
    int current_winner = 0;
    unsigned current_got_events = 0;

    while ( (got_events < nevents) && (bufs[winner]->got > 0) ) {
        for (int i=i_st; i<nfiles; ++i) {
            // read this file until hit limit timestamp
            while ( (bufs[i]->timestamp < limit_ts) && (bufs[i]->got > 0) ) {
                remaining = bufs[i]->got - bufs[i]->offset;

                if (dgram_size <= remaining) {
                    // get payload
                    d = (Dgram*)(bufs[i]->chunk + bufs[i]->offset);
                    payload = d->xtc.extent - xtc_size;
                    bufs[i]->offset += dgram_size;
                    remaining = bufs[i]->got - bufs[i]->offset;
                    
                    if (payload <= remaining) {
                        // got dgram :)
                        bufs[i]->offset += payload;
                        bufs[i]->nevents += 1;
                        bufs[i]->timestamp = ((unsigned long)d->seq.high << 32) | d->seq.low;
                    } else {
                        needs_reread = 1; // not enough for the whole block, shift and reread all files
                        break;
                    }
                } else {
                    needs_reread = 1; 
                    break;
                }

            } // while( (bufs[i]

            if (needs_reread == 1) {
                i_st = i; // start with the current buffer in the next round
                break;
            }

            // remember previous offsets in case reread is needed
            bufs[i]->prev_offset = bufs[i]->offset;
            
            if (bufs[i]->timestamp > current_max_ts) {
                current_max_ts = bufs[i]->timestamp;
                current_winner = i;
            }

            if (bufs[i]->nevents > current_got_events) {
                current_got_events = bufs[i]->nevents;
            }

        } // for (int i
        
        // shift and reread
        if (needs_reread == 1) {
            for (int j=0; j<bufs.size(); ++j) {
                bufs[j]->read_partial();
            }
            needs_reread = 0;
        } else {
            i_st = 0; // make sure that unless reread, always start with buffer 0
            winner = current_winner;
            limit_ts = current_max_ts + 1;
            got_events = current_got_events;
            current_got_events = 0;
        }
        
    } // while ( (got_events

}

