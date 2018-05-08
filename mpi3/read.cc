#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <time.h>
#include <unistd.h>

int main(){
    //clock_t begin = clock();
    char file_name[] = "/reg/d/psdm/cxi/cxid9114/scratch/mona/datafile.config";
    int fd = open(file_name, O_RDONLY);
    size_t nbytes = 8000000;
    char* buf = (char*)malloc(nbytes);
    int read_success = read(fd, buf, nbytes);
    if (read_success < 0) {
        printf("Error reading %s\n", file_name);
        return -1;
    }
    //free(buf);
    //clock_t end = clock();
    //double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    //printf("Time (s): %f\n", time_spent);
    return 0;
}
