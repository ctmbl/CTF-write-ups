#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc, char const *argv[])
{
    char flag[100];
    int fd = open("/flag", O_RDONLY);
    read(fd, flag, 100);
    write(fd, flag, stdout);
    
    return 0;
}
