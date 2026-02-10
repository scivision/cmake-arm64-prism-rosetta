#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <stdbool.h>

#ifdef __APPLE__
#include <sys/sysctl.h>
#endif

bool is_rosetta() {
#ifdef __APPLE__
    int ret = 0;
    size_t size = sizeof(ret);

    if (sysctlbyname("sysctl.proc_translated", &ret, &size, NULL, 0) < 0) {
        if (errno == ENOENT)
            return false;
        perror("sysctlbyname");
        return false;
    }

    return ret == 1;
#else
    return false;
#endif
}

int main(int argc, char **argv) {
    printf("%s is %susing Rosetta.\n", argv[0], is_rosetta() ? "" : "not ");
    return EXIT_SUCCESS;
}
