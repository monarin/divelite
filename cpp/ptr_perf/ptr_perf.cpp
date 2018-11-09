#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <time.h>
#include <vector>
#include <memory>
#include "dummy.h"
using namespace std;


class PtrPerf {
public:
    vector<shared_ptr<Dummy>> dummies;
    int n_dummies;

    PtrPerf(int _n_dummies) {
        n_dummies = _n_dummies;
        for (int i=0; i<n_dummies; ++i) {
            shared_ptr<Dummy> dummy(new Dummy{i});
            dummies.push_back(dummy);
        }
    }

    void multiply(int factor) {
        for (int i=0; i<n_dummies; ++i) {
            dummies[i]->multiply(factor);
        }      
    }
};

int main(int argc, char** argv) {
    int n_dummies = stoi(argv[1]);
    int n_loops = stoi(argv[2]);
    time_t st, en;

    time(&st);

    PtrPerf ptrp(n_dummies);
    for (int i=0; i<n_loops; ++i) {
        ptrp.multiply(1);
        for (int j=0; j<n_dummies; ++j) {
            cout << "i "<< i << " j " << j << " id " << ptrp.dummies[j]->id << endl;
            ptrp.dummies[j]->get(0);
        }
        
    }

    time(&en);
    double seconds = difftime(en, st);
    cout << "Total Elapsed (s)" << seconds << endl; 
} 

