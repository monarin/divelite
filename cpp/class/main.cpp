#include <sstream>
#include <iomanip>
#include <iostream>
#include <fcntl.h>
#include <string.h>
#include <vector>

#include "smdreader.h"

using namespace std;

int main() {
    string xtc_file;
    vector<int> fds;
    for (int i=0; i<3; i++) {
        stringstream ss;
        ss << setw(2) << setfill('0') << i;
        xtc_file = "/reg/d/psdm/xpp/xpptut15/scratch/mona/test/smalldata/data-"+ss.str()+".smd.xtc";
        int fd = open(xtc_file.c_str(), O_RDONLY);
        fds.push_back(fd);
        cout << "read " << xtc_file << " " << fd << endl;
    }

    SmdReader smdr(fds);
    smdr.get(1);

    //Buffer obj1(fd);
    //obj1.print_got();
    return 0;
}

