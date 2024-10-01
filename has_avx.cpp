// MacOS specific

#include <iostream>
#include <cstdlib>
#include <cerrno>

#include <sys/sysctl.h>


bool has_avx2(){
   int ret = 0;
   size_t size = sizeof(ret);

   if (sysctlbyname("hw.optional.avx2_0", &ret, &size, NULL, 0) < 0)
   {
      switch (errno){
        case ENOENT:
        case ENOTSUP:
          return false;
        default:
          throw;
      }
   }

   return (ret == 1);
}


int main() {

std::cout << (has_avx2() ? " has AVX2\n" : " does not have AVX2\n");

return EXIT_SUCCESS;
}
