#include <iostream>
#include <thread>
#include <vector>

using namespace std;

// This function will be called from a thread

void func(int tid) {
    cout << "Lanched by thread " << tid << endl;
}

int main() {
    vector<thread> th;
    int nr_threads = 10;

    // Launch a group of threads
    for (int i = 0; i < nr_threads; ++i) {
        th.push_back(thread(func, i));
    }

    // Join the threads with the main thread
    for (auto &t : th) {
        t.join();
    }

    return 0;
}

