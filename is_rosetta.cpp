#include <iostream>
#include <cerrno>
#include <cstdlib>

#ifdef __APPLE__
#include <sys/sysctl.h>
#endif

bool is_rosetta(){

#ifdef __APPLE__
   int ret = 0;
   size_t size = sizeof(ret);

   if (sysctlbyname("sysctl.proc_translated", &ret, &size, nullptr, 0) < 0)
   {
      if (errno == ENOENT)
         return false;
      throw;
   }

   return ret == 1;
#else
   return false;
#endif
}

int main(int argc, char ** argv) {

std::cout << argv[0] << " is " << (is_rosetta() ? "" : "not ") << "using Rosetta.\n";

  return EXIT_SUCCESS;
}
