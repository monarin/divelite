#include <sstream>
#include <iomanip>
#include <iostream>
#include <fcntl.h>
#include <string.h>
#include <vector>
#include <time.h>

#include "smdreader.h"

using namespace std;

int main(int argc, char** argv) {
    string xtc_file;
    vector<int> fds;
    int nfiles = stoi(argv[1]);
    for (int i=0; i<nfiles; i++) {
        stringstream ss;
        ss << setw(2) << setfill('0') << i;
        xtc_file = "/reg/d/psdm/xpp/xpptut15/scratch/mona/test/smalldata/data-"+ss.str()+".smd.xtc";
        int fd = open(xtc_file.c_str(), O_RDONLY);
        fds.push_back(fd);
    }
    
    time_t st, en;
    double seconds;
    time(&st);
    
    unsigned got_events = -1;
    SmdReader smdr(fds);
    
    unsigned processed_events = 0;
    while (got_events != 0) {
        smdr.get(1);
        got_events = smdr.got_events;
        processed_events += got_events;
    }

    time(&en);
    seconds = difftime(en, st);
    double rate = ((double)processed_events) / (seconds*1000000);
    cout << "Total Elapsed(s): " << seconds << " Processed Events: " << processed_events << " Rate(MHz): " << rate << endl; 
    cout << "DeltaT get_init(s): " << smdr.dt_get_init << endl;
    cout << "DeltaT get_dgram(s): " << smdr.dt_get_dgram << endl;
    cout << "DeltaT reread(s):" << smdr.dt_reread << endl;

    return 0;
}

