/* compile and run:
   g++ -pthread read_threads.cpp -o read_threads
   ./read_threads
*/
#include <iostream>
#include <iomanip>
#include <thread>
#include <vector>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>
#include <sstream>
#include <memory>
#include <unistd.h>
#include <time.h>

#define CHUNKSIZE 0x100000

using namespace std;

class Buffer {
public:
    char* chunk;
    int fd;

    Buffer(int _fd){
        fd = _fd;
        chunk = (char *)malloc(CHUNKSIZE);
        //cout << "malloc chunk " << &chunk << endl;
    }

    ~Buffer(){
        //cout << "free chunk " << &chunk << endl;
        free(chunk);
    }

    size_t reread() {
        size_t got = read(fd, chunk, CHUNKSIZE);
        return got;
    }
};

// This function will be called from a thread

void func(int tid, shared_ptr<Buffer> buf) {
    //cout << "Launched by thread " << tid << " for buf " << &(buf->chunk) << endl;
    size_t got = 1;
    while (got > 0) {
        got = buf->reread();
        //cout << "thread " << tid << " read " << got << endl;
    }
}

int main(int argc, char** argv) {
    string xtc_file;
    vector<int> fds;
    vector<shared_ptr<Buffer>> bufs;
    vector<thread> th;
    int nfiles = stoi(argv[1]);
    for (int i=0; i<nfiles; i++) {
        stringstream ss;
        ss << setw(2) << setfill('0') << i;
        xtc_file = "/reg/d/psdm/xpp/xpptut15/scratch/mona/xtc2/smalldata/data-r0001-s"+ss.str()+".smd.xtc2";
        int fd = open(xtc_file.c_str(), O_RDONLY);
        fds.push_back(fd);
        
        shared_ptr<Buffer> buf(new Buffer{fd});
        bufs.push_back(buf);
    }

    time_t st, en;
    time(&st);

    // Launch a group of threads
    for (int i = 0; i < nfiles; ++i) {
        th.push_back(thread(func, i, bufs[i]));
    }

    // Join the threads with the main thread
    for (auto &t : th) {
        t.join();
    }
    
    time(&en);
    double seconds = difftime(en, st);
    cout << "Total Elapsed (s): " << seconds << " Bandwidth (GB/s):" << 14/seconds << endl;
    return 0;
}

