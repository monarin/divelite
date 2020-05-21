#include <iostream>
#include <thread>
#include <vector>
#include <sys/time.h>

using namespace std;

// This function will be called from a thread

void func(int tid) {
    int a;
    a=tid;
    //cout << "Lanched by thread " << tid << endl;
}

int main() {
    vector<thread> th;
    int nr_threads = 10;
    struct timeval tv_st, tv_en;


    // Launch a group of threads
    for (int i = 0; i < nr_threads; ++i) {
        th.push_back(thread(func, i));
    }
    gettimeofday(&tv_st, NULL);

    // Join the threads with the main thread
    for (auto &t : th) {
        t.join();
    }

    gettimeofday(&tv_en, NULL);
    unsigned long ut_st, ut_en;
    ut_st = 1000000 * tv_st.tv_sec + tv_st.tv_usec;
    ut_en = 1000000 * tv_en.tv_sec + tv_en.tv_usec;
    cout << ut_st << " " << ut_en << " " << ut_en - ut_st << endl;

    return 0;
}

