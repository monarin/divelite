#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int main()
{
    char *arr;  int i;
    arr = (char *)malloc(sizeof(char)*5);
    strcpy(arr, "amee is my name");
    return 0;
}
