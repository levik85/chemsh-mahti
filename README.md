# Chemshell-py 20.0.2 quick configuration for mahti servers

  Install chemshell-py and link to both aims and gulp on CSC's mahti server

  By [Levi Keller](levi.keller@aalto.fi)

## STEP 0: load modules

  * ml cmake netlib-scalapack

  * Together with the default congfiguration this should give you :

   1. gcc/9.3.0   
   1. openmpi/4.0.3   
   1. openblas/0.3.10   
   1. StdEnv   
   1. netlib-scalapack/2.1.0   
   1. cmake/3.16.2

  note that if the default configuration changes you will have to modify the enclosed mahti.sh accordingly to ensure that all but cmake/3.16.2 are available at runtime

  * Install numpy in userspace:
  `pip3 install --user numpy`


## STEP 1: prepare files

  1. download chemsh-py-20.0.2 and untar/zip to `$CHSHROOT`
   * copy the enclosed `mahti.*` to `$CHSHROOT/chemsh/utils/platforms`
  1. download gulp-5.2 and untar/zip to `$GULPROOT`
  1. Download FHIaims to `$AIMSROOT`
   * copy supplied `make.sys` to `$AIMSROOT/src`
   * go to $AIMSROOT and issue `make -j libaims.scalapack.mpi`
   * this will build the target `$AIMSROOT/lib/libaims.$AIMS_VN.scalapack.mpi.so`
   
   * _**alternatively**_ (assuming all licensing issues are in order) you can ask me for a recent .so file
  
## STEP 2: Edit files

  1. In `$CHSHROOT/setup` search for `-O` and add `type=int,` to the argument list on the succeeeding lines (e.g. line 163)
  1. on line 772 (or 773 after the above edit) replace 'make' with 'make VERBOSE=1'
  *This will allow you to identify the location of missed occurences of lapack in the following step*     
  1. In `$CHSHROOT/chemsh/` and all its subdirectories search through the `CMakeLists.txt` files and whereever you find
   `target_link_libraries(arg1 arg2 ...)` where any of the arguments is `lapack`, change it to `openblas`

## STEP 3: compile

  * Go to `$CHSHROOT` and issue
 
    ./setup -O 3 -j 24 --platform mahti --gulp $GULPROOT  --gulp-version 5.2 --fhiaims $AIMSROOT/lib/libaims.$AIMS_VN.scalapack.mpi.so


## STEP 4: run

   * The validation test scripts in `$CHSHROOT/tests` are incompatible with python without further modification
   * The hook in dl-find is not working

   1. Go to the directory of the validation test you are interested in and issue
   
    $CHSHROOT/bin/gnu/chemsh --submit -pl mahti -np np -A your_account -J jobname -N partition file_to_test.py

   1. Check output: jobname.err and jobname.log
   1. For further control command line options, see the output of
   
    $CHSHROOT/bin/gnu/chemsh -h
