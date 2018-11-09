#include <cstddef>

#define CHUNKSIZE 0x100000

class Dummy {
public:
    int id;
    char* chunk;

    Dummy(int _id);
    ~Dummy();
    void multiply(int factor);
    void get(size_t offset);
};
