# Chemshell-py 20.0.2 configuration for mahti servers

  Install chemshell-py and link to both aims and gulp on CSC's mahti server
  [Levi Keller](levi.keller@aalto.fi)

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

  * download chemsh-py-20.0.2 and untar/zip to `$CHSHROOT`
  * copy the enclosed `mahti.*` to `$CHSHROOT/chemsh/utils/platforms`
 
  download gulp-5.2 and untar/zip to `$GULPROOT`

   Download FHIaims to `$AIMSROOT`
   copy supplied `make.sys` to `$AIMSROOT/src`
   go to $AIMSROOT and issue `make -j libaims.scalapack.mpi`
   this will build the target `$AIMSROOT/lib/libaims.$AIMS_VN.scalapack.mpi.so`
   --- alternatively ask me for a recent .so files ---

## STEP 2: Edit files

    Edit `$CHSHROOT/setup`
    search for `-O` add `type=int,` to the argument list on the succeeeding lines (e.g. line 163)
    on line 772 (or 773 after the above edit) replace 'make' with 'make VERBOSE=1'
     
    In `$CHSHROOT/chemsh/` and all its subdirectories search through the `CMakeLists.txt` files and whereever you find
    `target_link_libraries(arg1 arg2 ...)` where any of the arguments is `lapack`, change it to `openblas`

## STEP 3: compile

    in `$CHSHROOT` issue
 
     `./setup -O 3 -j 24 --platform mahti --gulp $GULPROOT  --gulp-version 5.2 --fhiaims $AIMSROOT/lib/libaims.$AIMS_VN.scalapack.mpi.so`


## STEP 4: run

   the validation test scripts in `$CHSHROOT/tests` are incompatible with python without further modification
   the hook in dl-find is not working

   go to the directory of the validation test you are interested in and issue
   `$CHSHROOT/bin/gnu/chemsh --submit -pl mahti -np np -A your_account -J jobname -N partition file_to_test.py`

   check output: jobname.err and jobname.log
   for further control command line options, use the
   `$CHSHROOT/bin/gnu/chemsh -h`