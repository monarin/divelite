// array of strings example
// from https://www.geeksforgeeks.org/array-strings-c-3-different-ways-create/
#include <iostream>
#include <string>
#include <vector>
#include <array>

using namespace std;


int main()
{
    // 1. Using Pointers (fixed-length array, immutable strings)
    const char* color1[4] = {"Blue", "Red", "Orange", "Yellow"};

    // 2. Using 2D array (fixed-length array, immutable/fixed-size strings)
    char color2[4][10] = {"Blue", "Red", "Orange", "Yellow"};

    // 3. Using the string class (fixed-length array, mutable/variable-isze strings)
    string color3[4] = {"Blue", "Red", "Orange", "Yellow"};
    color3[1] = "Black";

    // 4. Using the vector class (variable-lenth array, mutable/variable-size strings)
    // Note: initializer shown in the original example doesn't work with pre c++11
    vector<string> color4;
    color4.push_back("Yellow");

    for (int i=0; i<color4.size(); i++)
        cout << color4[i] << endl;

    // 5. Using the array class (fixed-size array)
    // array needs c++11 g++ ex-01-array-of-strings.cc -o ex-01-array-of-strings -std=c++11
    array<string, 4> color5;
    color5[0] = "Blue";
    color5[1] = "Red";
    color5[2] = "Orange";
    color5[3] = "Yellow";
    
    for (int i=0; i < 4; i++) 
        cout << color1[i] << " " << color2[i] << " " << color3[i] << " " << color5[i] <<  endl;

    return 0;
}
