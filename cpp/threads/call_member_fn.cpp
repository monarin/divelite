// Use a member function in a thread
#include <iostream>
#include <thread>
#include <string>

using namespace std;

class SayHello{
public:

    // This function will be called from a thread
    void func(const string &name) {
        cout << "Hello " << name << endl;
    };
};

int main(int argc, char* argv[])
{
    SayHello x;

    // Use a member fucntion in a thread
    thread t(&SayHello::func, &x, "Tom");

    // Join the thread with the main thread
    t.join();

    return 0;
}
