#include <iostream>
using namespace std;
 
class ReferenceCounter
{ 
public: 
    int count;
    char* buf;
         
    // Default Constructor
    ReferenceCounter() {
        count = 0;
        buf = (char *) malloc(10);
    }

    ReferenceCounter(const ReferenceCounter &rc) {
        cout << "copy constructor called" << endl;
        count = rc.count + 1;
    }

    ~ReferenceCounter() {
        if (count == 0) {
            cout << "free buf" << endl;
            free(buf);
        }
    }
};
 
int main()
{
    ReferenceCounter a;
    cout << "a count: "<< a.count << endl;
    ReferenceCounter b = a;
    cout << "b count: "<< b.count << endl;
    return 1;
}

