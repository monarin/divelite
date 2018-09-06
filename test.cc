#include <sys/time.h>
#include <stdio.h>

int main() {
    struct timeval tv0, tv1;
    gettimeofday(&tv0, NULL);
    printf("%d\n",tv0.tv_sec);
    printf("%d\n",tv0.tv_usec);
    gettimeofday(&tv1, NULL);
    printf("%d\n",tv1.tv_sec);
    printf("%d\n",tv1.tv_usec);
    printf("%d\n", tv1.tv_sec - tv0.tv_sec);
    printf("%d\n", tv1.tv_usec - tv0.tv_usec);
}
