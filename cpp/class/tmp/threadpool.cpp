#include <vector>
#include <queue>
#include <memory>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <future>
#include <functional>
#include <stdexcept>

using namespace std;

class ThreadPool {
public:
    ThreadPool(size_t);
    template<class F, class.. Args>
    auto enqueue(F&& f, Args&&... args)
        -> future<typename result_of<F(Args...)>::type>;
    ~ThreadPool();

private:
    // need to keep track of threads so we can join them
    vector<thread> workers;
    // the task queue
    queue<function<void()> > tasks;

    // synchronization
    mutex queue_mutex;
    condition_variable condition;
    bool stop;
};

// the constructor just launches some amount of workers
inline ThreadPool::ThreadPool(size_t threads)
    : stop(false)
{
    for (size_t i=0; i<threads; ++i)
        workers.em
