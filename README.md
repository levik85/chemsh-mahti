- Install chemshell-py and link to both aims and gulp on CSC's mahti server
- Levi.Keller@Aalto.fi

STEP 0: load modules

   ml cmake netlib-scalapack

   together with the default congfiguration this should give you :

  1) gcc/9.3.0   2) openmpi/4.0.3   3) openblas/0.3.10   4) StdEnv   5) netlib-scalapack/2.1.0   6) cmake/3.16.2

  note that if the default configuration changes you will have to modify the enclosed mahti.sh accordingly to ensure that all but #6 are available at runtime


STEP 1: prepare files

# download chemsh-py-20.0.2 and untar/zip to $CHSHROOT
  copy the enclosed mahti.* to $CHSHROOT/chemsh/utils/platforms
 
# download gulp-5.2 and untar/zip to $GULPROOT

#  Download aims to $AIMSROOT
   copy supplied make.sys to $AIMSROOT/src
   go to $AIMSROOT and issue make -j libaims.scalapack.mpi
   this will build the target $AIMSROOT/lib/libaims.$AIMS_VN.scalapack.mpi.so
   --- alternatively ask me for a recent .so files ---

STEP 2: Edit files

#   Edit $CHSHROOT/setup
    search for '-O' add 'type=int,' to the argument list on the succeeeding lines (e.g. line 163)
    on line 772 (or 773 after the above edit) replace 'make' with 'make VERBOSE=1'
     
    In $CHSHROOT/chemsh/ and all its subdirectories search through the CMakeLists.txt files and whereever you find
    'target_link_libraries(arg1 arg2 ...)' where any of the arguments is lapack, change it to openblas

STEP 3: compile

    in $CHSHROOT issue
 
  {{ ./setup -O 3 -j 24 --platform mahti --gulp $GULPROOT  --gulp-version 5.2 --fhiaims $AIMSROOT/lib/libaims.$AIMS_VN.scalapack.mpi.so  }}


