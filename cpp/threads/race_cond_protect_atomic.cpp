#include <iostream>
#include <thread>
#include <vector>
#include <atomic>

using namespace std;

//Split "mem" into "parts", e.g. if mem = 10 and parts = 4 you will have: 0,2,4,6,10
//if possible the function will split mem into equal chuncks, if not 
//the last chunck will be slightly larger
vector<int> bounds(int parts, int mem) {
    vector<int>bnd;
    int delta = mem/ parts;
    int remainder = mem % parts;
    int N1=0, N2=0;
    bnd.push_back(N1);
    for (int i=0; i<parts; ++i) {
        N2 = N1 + delta;
        if (i == parts - 1)
            N2 += remainder;
        bnd.push_back(N2);
        N1=N2;
    }
    return bnd;
}

void dot_product(const vector<int> &v1, const vector<int> &v2, 
        atomic<int> &result, int L, int R)
{
    int partial_sum = 0;
    for (int i=L; i<R; ++i) {
        partial_sum += v1[i] * v2[i];
    }
    result += partial_sum;
}

int main(){
    int nr_elements = 100000;
    int nr_threads = 2;
    atomic<int> result(0);
    vector<thread> threads;

    // Fill two vectors with some constant values for a quick verification
    // v1={1,1,...}
    // v2={2,2,...}
    // The result of the dot_product should be 200000 for this particular case
    vector<int> v1(nr_elements, 1), v2(nr_elements, 2);

    // Split nr_elements into nr_threads parts
    vector<int> limits = bounds(nr_threads, nr_elements);

    // Launch nr_threads threads
    for (int i=0; i<nr_threads; ++i) {
        threads.push_back(thread(dot_product, ref(v1), ref(v2), ref(result), 
                    limits[i], limits[i+1]));
    }

    // Join the threads with the main thread
    for (auto &t: threads){
        t.join();
    }

    cout << result << endl;
    return 0;
}
